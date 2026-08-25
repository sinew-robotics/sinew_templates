# RSS 2026

Verified: 2026-08-25
Official source: [Presenter Information](https://roboticsconference.org/information/presentationInstructions/)

## Verified delivery requirements

- Four-minute plenary oral for every accepted paper, plus poster.
- Mandatory pre-submitted, self-advancing video no longer than 240 seconds.
- Exactly 1920x1080 MPEG-4 named `Paper_X.m4v`.
- Presenter speaks live while the video runs.
- No narration/audio except experimental sound needed to understand the result, unless a rare remote exception is approved.

Q&A occurs for papers together at the end of the technical session rather than inside each four-minute video.

## Branding evidence

The official page does not mandate fonts, palette, slide template, or logo. The submitted video must use the required 1920x1080 canvas; visual-style selection remains independent.

## Production workflow

Reveal HTML is useful for authoring, but the submitted artifact is a deterministic video. Rehearse narration first, then assign per-slide timing. Verify that every transition, video, and animation completes without input and that the last frame does not overrun 240 seconds.

Recommended gates:

- export at 1920x1080 using a standards-compatible MPEG-4/H.264 workflow;
- inspect duration with `ffprobe` rather than a media player's rounded display;
- listen for accidental narration/system audio;
- rehearse live narration against the immutable video;
- bring a local copy and the exact submitted version.
