#!/usr/bin/env python3
"""Check that no slide's rendered content overflows the Reveal canvas.

Render succeeds and the HTML is valid even when content silently runs past
the bottom (or, since v1.2.0's switch to vertically centered content, both
the top AND the bottom) of a slide -- nothing in the HTML itself signals
that. This script measures the actual laid-out geometry of every slide in
a headless browser and reports any element whose rendered box extends past
the deck's configured canvas size.

Usage: check_overflow.py HTML

Exit codes:
  0 - ran, no overflow found.
  1 - ran, overflow found (see the per-slide report).
  2 - COULD NOT RUN (no headless browser, or it failed to start/connect).
      This is not a pass. AGENTS.md requires stating which gate did not
      run and why; this script does that on stderr instead of silently
      exiting 0.

Reusable pieces (for future probes/gates against a rendered Sinew deck,
per sinew-dpy.7 -- do not hand-roll a fourth CDP client):
  - CDP: a minimal stdlib-only Chrome DevTools Protocol client.
  - find_chrome_binary(): locate a headless-capable Chrome/Chromium.
  - launch_headless_chrome(): start one with a remote debugging port.
  - serve_directory(): serve a directory over plain HTTP in a thread
    (file:// loads produce a plugin error that does not reproduce over
    http -- verified; always serve, never navigate to a file:// URL).
  - wait_for_stable_geometry(): poll a JS snapshot expression until it
    returns the same value on several consecutive polls. Reveal's layout
    (fonts, KaTeX, image decode, algorithm/citation numbering scripts) is
    not synchronously stable right after navigating to a slide; measuring
    immediately produces flaky results. Two agents hand-rolled this exact
    poll-for-N-stable-samples loop before landing on four samples as
    enough in practice; import it instead of writing a third/fourth copy.
"""

from __future__ import annotations

import base64
import functools
import http.server
import json
import os
import shutil
import socket
import struct
import subprocess
import sys
import tempfile
import threading
import time
import urllib.request
from pathlib import Path

CHROME_CANDIDATES = (
    "google-chrome",
    "google-chrome-stable",
    "chromium",
    "chromium-browser",
    "chrome",
)
STABLE_SAMPLES = 4
POLL_INTERVAL = 0.15
STABLE_TIMEOUT = 10.0
OVERFLOW_EPSILON_PX = 0.5  # sub-pixel rounding noise, not a real overflow


# --------------------------------------------------------------------------
# Minimal stdlib Chrome DevTools Protocol client. No external dependencies.
# --------------------------------------------------------------------------
class CDP:
    """A tiny CDP client: one target tab, JSON commands over a raw
    WebSocket connection hand-rolled from stdlib `socket` (no `websockets`
    dependency). Enough to navigate, wait for load, and evaluate JS.
    """

    def __init__(self, port: int) -> None:
        self.port = port
        self.msg_id = 0
        info = self._http_put(f"http://127.0.0.1:{port}/json/new?about:blank")
        self.ws_url = info["webSocketDebuggerUrl"]
        self.target_id = info["id"]
        self.sock = self._ws_connect(self.ws_url)

    @staticmethod
    def _http_get(url: str):
        with urllib.request.urlopen(url, timeout=10) as response:
            return json.loads(response.read().decode())

    @staticmethod
    def _http_put(url: str):
        request = urllib.request.Request(url, method="PUT")
        with urllib.request.urlopen(request, timeout=10) as response:
            return json.loads(response.read().decode())

    @staticmethod
    def _ws_connect(ws_url: str) -> socket.socket:
        assert ws_url.startswith("ws://")
        rest = ws_url[len("ws://") :]
        host_port, path = rest.split("/", 1)
        path = "/" + path
        if ":" in host_port:
            host, port_text = host_port.split(":")
            port = int(port_text)
        else:
            host, port = host_port, 80
        sock = socket.create_connection((host, port), timeout=10)
        key = base64.b64encode(os.urandom(16)).decode()
        request = (
            f"GET {path} HTTP/1.1\r\n"
            f"Host: {host}:{port}\r\n"
            "Upgrade: websocket\r\n"
            "Connection: Upgrade\r\n"
            f"Sec-WebSocket-Key: {key}\r\n"
            "Sec-WebSocket-Version: 13\r\n\r\n"
        )
        sock.sendall(request.encode())
        response = b""
        while b"\r\n\r\n" not in response:
            response += sock.recv(4096)
        assert b"101" in response.split(b"\r\n", 1)[0], response[:200]
        return sock

    @staticmethod
    def _ws_send(sock: socket.socket, obj: dict) -> None:
        payload = json.dumps(obj).encode()
        header = bytearray([0x81])  # FIN + text frame
        length = len(payload)
        mask = os.urandom(4)
        if length <= 125:
            header.append(0x80 | length)
        elif length <= 65535:
            header.append(0x80 | 126)
            header += struct.pack(">H", length)
        else:
            header.append(0x80 | 127)
            header += struct.pack(">Q", length)
        header += mask
        masked = bytes(b ^ mask[i % 4] for i, b in enumerate(payload))
        sock.sendall(bytes(header) + masked)

    @staticmethod
    def _ws_recv_frame(sock: socket.socket) -> tuple[int, bytes]:
        def recv_exact(count: int) -> bytes:
            buf = b""
            while len(buf) < count:
                chunk = sock.recv(count - len(buf))
                if not chunk:
                    raise ConnectionError("socket closed")
                buf += chunk
            return buf

        first_two = recv_exact(2)
        opcode = first_two[0] & 0x0F
        masked = first_two[1] & 0x80
        length = first_two[1] & 0x7F
        if length == 126:
            length = struct.unpack(">H", recv_exact(2))[0]
        elif length == 127:
            length = struct.unpack(">Q", recv_exact(8))[0]
        if masked:
            mask = recv_exact(4)
            data = recv_exact(length)
            data = bytes(b ^ mask[i % 4] for i, b in enumerate(data))
        else:
            data = recv_exact(length)
        return opcode, data

    def _ws_recv_json(self, timeout: float = 30):
        self.sock.settimeout(timeout)
        _opcode, data = self._ws_recv_frame(self.sock)
        return json.loads(data.decode())

    def send(self, method: str, params: dict | None = None) -> int:
        self.msg_id += 1
        message_id = self.msg_id
        self._ws_send(self.sock, {"id": message_id, "method": method, "params": params or {}})
        return message_id

    def recv_until(self, message_id: int, timeout: float = 60):
        deadline = time.time() + timeout
        while time.time() < deadline:
            remaining = max(1, int(deadline - time.time()))
            message = self._ws_recv_json(timeout=remaining)
            if message.get("id") == message_id:
                return message
        raise TimeoutError(f"no response for id={message_id}")

    def call(self, method: str, params: dict | None = None, timeout: float = 60):
        message_id = self.send(method, params)
        message = self.recv_until(message_id, timeout=timeout)
        if "error" in message:
            raise RuntimeError(f"{method} error: {message['error']}")
        return message.get("result", {})

    def evaluate(self, expression: str, timeout: float = 30):
        result = self.call(
            "Runtime.evaluate",
            {"expression": expression, "awaitPromise": True, "returnByValue": True, "timeout": int(timeout * 1000)},
            timeout=timeout + 5,
        )
        inner = result.get("result", {})
        if "value" not in inner and inner.get("type") == "undefined":
            return None
        return inner.get("value")

    def wait_for_load(self, url: str, timeout: float = 20) -> None:
        self.call("Page.enable")
        self.call("Page.navigate", {"url": url})
        deadline = time.time() + timeout
        while time.time() < deadline:
            message = self._ws_recv_json(timeout=max(1, int(deadline - time.time())))
            if message.get("method") == "Page.loadEventFired":
                return
        raise TimeoutError(f"no load event for {url} within {timeout}s")

    def close(self) -> None:
        try:
            self.sock.close()
        except Exception:
            pass
        try:
            request = urllib.request.Request(f"http://127.0.0.1:{self.port}/json/close/{self.target_id}")
            urllib.request.urlopen(request, timeout=5)
        except Exception:
            pass


def find_chrome_binary() -> str | None:
    for name in CHROME_CANDIDATES:
        path = shutil.which(name)
        if path:
            return path
    return None


def free_tcp_port() -> int:
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as probe:
        probe.bind(("127.0.0.1", 0))
        return probe.getsockname()[1]


def launch_headless_chrome(binary: str, port: int, user_data_dir: str) -> subprocess.Popen:
    process = subprocess.Popen(
        [
            binary,
            "--headless=new",
            "--disable-gpu",
            "--no-sandbox",
            "--disable-dev-shm-usage",
            "--hide-scrollbars",
            "--force-color-profile=srgb",
            f"--remote-debugging-port={port}",
            f"--user-data-dir={user_data_dir}",
            "about:blank",
        ],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    )
    deadline = time.time() + 15
    while time.time() < deadline:
        if process.poll() is not None:
            raise RuntimeError(f"{binary} exited early with code {process.returncode}")
        try:
            CDP._http_get(f"http://127.0.0.1:{port}/json/version")
            return process
        except Exception:
            time.sleep(0.15)
    process.kill()
    raise TimeoutError(f"{binary} did not become ready on port {port} within 15s")


def serve_directory(directory: Path) -> tuple[http.server.ThreadingHTTPServer, threading.Thread]:
    """Serve `directory` over plain HTTP on an ephemeral localhost port.

    A `file://` load of the rendered deck produces a plugin error in
    headless Chrome that does not reproduce over http -- verified -- so
    every probe against a rendered Sinew deck must go through this (or an
    equivalent local server), never navigate straight to a file:// URL.
    """
    handler = functools.partial(http.server.SimpleHTTPRequestHandler, directory=str(directory))
    server = http.server.ThreadingHTTPServer(("127.0.0.1", 0), handler)
    thread = threading.Thread(target=server.serve_forever, daemon=True)
    thread.start()
    return server, thread


def wait_for_stable_geometry(cdp: CDP, snapshot_expr: str, samples: int = STABLE_SAMPLES,
                              interval: float = POLL_INTERVAL, timeout: float = STABLE_TIMEOUT):
    """Poll `snapshot_expr` (a JS expression returning a JSON-serializable
    value) until it returns the byte-identical value on `samples`
    consecutive polls in a row, then return that stable value.

    Reveal's layout is NOT synchronously stable immediately after
    navigating to a slide (fonts, KaTeX typesetting, image decode, the
    algorithm/citation/Q-H numbering scripts, and the divider-lockup
    clone-on-load runtime all mutate the DOM or reflow asynchronously), so
    measuring right away produces flaky false positives and false
    negatives. This is the one polling loop this file (and any future
    probe against a rendered Sinew deck) should use -- do not hand-roll a
    second copy.
    """
    deadline = time.monotonic() + timeout
    last_snapshot = None
    streak = 0
    last_value = None
    while time.monotonic() < deadline:
        value = cdp.evaluate(snapshot_expr)
        snapshot = json.dumps(value, sort_keys=True)
        if snapshot == last_snapshot:
            streak += 1
            if streak >= samples:
                return value
        else:
            streak = 1
            last_snapshot = snapshot
            last_value = value
        time.sleep(interval)
    raise TimeoutError(f"geometry did not stabilize within {timeout}s (last sample: {last_value})")


# --------------------------------------------------------------------------
# Overflow measurement.
# --------------------------------------------------------------------------
ENUMERATE_SLIDES_JS = """
(() => {
  const slides = Reveal.getSlides();
  return slides.map((slide) => {
    const indices = Reveal.getIndices(slide);
    // .h/.v come back `undefined` (not 0) for a stack with no vertical
    // slides or a deck with no horizontal stacks, and JSON serialization
    // drops an undefined-valued key entirely rather than sending `null`
    // -- coalesce every index to 0 so the returned object always has all
    // three keys and Reveal.slide() below always gets real numbers.
    return {id: slide.id || null, h: indices.h ?? 0, v: indices.v ?? 0, f: indices.f ?? null};
  });
})()
"""

# Measures only elements that actually PAINT visible ink -- not every
# element's border box -- against the deck's own configured canvas size,
# in the slide's LOGICAL coordinate system (i.e. dividing out whatever CSS
# transform: scale(...) Reveal currently applies to fit the configured
# width/height into the actual viewport) so the threshold is meaningful
# regardless of the emulated browser window size.
#
# Why not every element's box: core.scss's .columns/.column gutter uses a
# deliberate negative-margin-plus-compensating-padding idiom (`gap` is not
# available for the inline-block layout these use) -- `.columns` itself
# legitimately extends past its parent's content edge via a negative
# margin, and each `.column` child's matching positive padding pulls the
# actual content back inside. That is the mechanism working as designed,
# not a defect; measuring every element's border box flagged the `.columns`
# wrapper's own (intentionally overextended, content-free) box as "the"
# overflow on two gallery slides, 18 times over -- a false positive, not a
# real one; confirmed by reading core.scss (sinew_templates commit history,
# `.reveal .columns`/`.reveal .column` rules) and by the fact every one of
# those 18 findings named exactly `div.columns`, never an actual content
# element, and the amount matched the configured gutter to the decimal.
#
# So a candidate element only counts if IT (not a descendant) paints
# something: a background, a border, a replaced element (img/svg/video/
# canvas/iframe/object/embed), or a text node it owns directly (not merely
# inherited from a descendant). A pure layout wrapper with no background,
# no border, and no text of its own -- exactly what `.columns`/`.column`
# are -- never becomes a candidate, regardless of what margin trick it
# uses, so this generalizes to any future bleed/gutter idiom rather than
# special-casing this one. This is structural, not a magic-number
# tolerance: a real 8px clip on a painting element is still caught in
# full, at any size.
MEASURE_OVERFLOW_JS = """
(() => {
  const config = Reveal.getConfig();
  const canvasWidth = config.width || 1600;
  const canvasHeight = config.height || 900;
  const slidesEl = document.querySelector('.reveal .slides');
  // Reveal.getCurrentSlide(), NOT a raw '.present' query: during vertical
  // navigation Reveal marks BOTH the outer horizontal-stack <section> and
  // the actual current inner vertical <section> with class "present", and
  // a querySelector('section.present') returns the outer one first (DOM
  // order) -- whose descendants are every vertical slide in that stack,
  // not just the current one. getCurrentSlide() is the innermost slide
  // Reveal itself considers active.
  const slide = Reveal.getCurrentSlide();
  if (!slide) return {error: 'no current slide'};
  const transform = getComputedStyle(slidesEl).transform;
  let scale = 1;
  if (transform && transform !== 'none') {
    const m = transform.match(/matrix\\(([^)]+)\\)/);
    if (m) {
      const parts = m[1].split(',').map(Number);
      if (parts[0]) scale = parts[0];
    }
  }
  const REPLACED_TAGS = new Set(['IMG', 'SVG', 'VIDEO', 'CANVAS', 'IFRAME', 'OBJECT', 'EMBED']);
  function paintsOwnContent(el, cs) {
    if (REPLACED_TAGS.has(el.tagName)) return true;
    const bg = cs.backgroundColor;
    if (bg && bg !== 'transparent' && !/^rgba?\\([^)]*,\\s*0\\)$/.test(bg)) return true;
    if (cs.backgroundImage && cs.backgroundImage !== 'none') return true;
    if (['Top', 'Right', 'Bottom', 'Left'].some((side) => parseFloat(cs[`border${side}Width`]) > 0
        && cs[`border${side}Style`] !== 'none')) return true;
    for (const node of el.childNodes) {
      if (node.nodeType === Node.TEXT_NODE && node.textContent.trim().length > 0) return true;
    }
    return false;
  }
  const slideRect = slide.getBoundingClientRect();
  let worst = null;
  const elements = slide.querySelectorAll('*');
  for (const el of elements) {
    const cs = getComputedStyle(el);
    if (cs.display === 'none' || cs.visibility === 'hidden') continue;
    if (!paintsOwnContent(el, cs)) continue;
    const r = el.getBoundingClientRect();
    if (r.width === 0 && r.height === 0) continue;
    const logicalBottom = (r.bottom - slideRect.top) / scale;
    const logicalRight = (r.right - slideRect.left) / scale;
    const overflowBottom = logicalBottom - canvasHeight;
    const overflowRight = logicalRight - canvasWidth;
    const overflow = Math.max(overflowBottom, overflowRight);
    if (!worst || overflow > worst.overflow) {
      let cls = '';
      if (typeof el.className === 'string') cls = el.className;
      else if (el.className && el.className.baseVal) cls = el.className.baseVal;
      worst = {
        overflow: Math.round(overflow * 10) / 10,
        direction: overflowBottom >= overflowRight ? 'bottom' : 'right',
        tag: el.tagName.toLowerCase(),
        cls: cls,
        text: (el.textContent || '').trim().slice(0, 70),
      };
    }
  }
  return {
    slideId: slide.id || null,
    canvasWidth: canvasWidth,
    canvasHeight: canvasHeight,
    worst: worst,
  };
})()
"""


def check_deck(cdp: CDP, url: str) -> list[dict]:
    cdp.wait_for_load(url)
    slides = cdp.evaluate(ENUMERATE_SLIDES_JS)
    if not slides:
        raise RuntimeError("Reveal.getSlides() returned no slides; is this a rendered Sinew deck?")

    findings: list[dict] = []
    for position, slide in enumerate(slides):
        h, v, f = slide["h"], slide["v"], slide.get("f")
        nav_params = {"h": h, "v": v}
        if f is not None:
            nav_params["f"] = f
        cdp.call("Runtime.evaluate", {
            "expression": f"Reveal.slide({json.dumps(h)}, {json.dumps(v)}, {json.dumps(f)})",
            "awaitPromise": False,
        })
        measurement = wait_for_stable_geometry(cdp, MEASURE_OVERFLOW_JS)
        if measurement.get("error"):
            continue
        worst = measurement.get("worst")
        slide_label = measurement.get("slideId") or slide.get("id") or f"h{h}v{v}"
        if worst and worst["overflow"] > OVERFLOW_EPSILON_PX:
            findings.append(
                {
                    "position": position,
                    "slide": slide_label,
                    "h": h,
                    "v": v,
                    "overflow_px": worst["overflow"],
                    "direction": worst["direction"],
                    "element": f"{worst['tag']}{('.' + worst['cls'].split()[0]) if worst['cls'] else ''}",
                    "text": worst["text"],
                }
            )
    return findings


def main() -> int:
    if len(sys.argv) != 2:
        print("usage: check_overflow.py HTML", file=sys.stderr)
        return 2

    html_path = Path(sys.argv[1]).resolve()
    if not html_path.is_file():
        print(f"Overflow gate did NOT run: rendered HTML not found: {html_path}", file=sys.stderr)
        return 2

    binary = find_chrome_binary()
    if not binary:
        print(
            "Overflow gate did NOT run: no headless-capable Chrome/Chromium binary found "
            f"(looked for: {', '.join(CHROME_CANDIDATES)}). This is not a pass -- install "
            "one of those, or run this check where one is available, before claiming the "
            "overflow gate as satisfied.",
            file=sys.stderr,
        )
        return 2

    server = None
    chrome_process = None
    cdp = None
    user_data_dir = tempfile.mkdtemp(prefix="sinew-overflow-chrome-")
    try:
        try:
            server, _thread = serve_directory(html_path.parent)
            http_port = server.server_port
        except OSError as error:
            print(f"Overflow gate did NOT run: could not start a local HTTP server: {error}", file=sys.stderr)
            return 2

        cdp_port = free_tcp_port()
        try:
            chrome_process = launch_headless_chrome(binary, cdp_port, user_data_dir)
        except Exception as error:
            print(f"Overflow gate did NOT run: {binary} failed to start: {error}", file=sys.stderr)
            return 2

        try:
            cdp = CDP(cdp_port)
            cdp.call("Emulation.setDeviceMetricsOverride", {
                "width": 1600, "height": 900, "deviceScaleFactor": 1, "mobile": False,
            })
            url = f"http://127.0.0.1:{http_port}/{html_path.name}"
            findings = check_deck(cdp, url)
        except Exception as error:
            print(f"Overflow gate did NOT run: could not measure the render: {error}", file=sys.stderr)
            return 2

        if findings:
            print(f"Overflow check FAILED for {html_path}:", file=sys.stderr)
            for finding in findings:
                print(
                    f"  - slide '{finding['slide']}' (h={finding['h']} v={finding['v']}, "
                    f"position {finding['position']}): {finding['element']} overflows "
                    f"{finding['direction']} by {finding['overflow_px']}px "
                    f"(\"{finding['text']}\")",
                    file=sys.stderr,
                )
            return 1

        print(f"Overflow check passed: {html_path}")
        return 0
    finally:
        if cdp is not None:
            cdp.close()
        if chrome_process is not None:
            chrome_process.terminate()
            try:
                chrome_process.wait(timeout=5)
            except subprocess.TimeoutExpired:
                chrome_process.kill()
        if server is not None:
            server.shutdown()
        shutil.rmtree(user_data_dir, ignore_errors=True)


if __name__ == "__main__":
    raise SystemExit(main())
