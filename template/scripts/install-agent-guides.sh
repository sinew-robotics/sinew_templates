#!/usr/bin/env bash
set -euo pipefail

repo_dir="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")/.." && pwd)"

if [[ -e "$repo_dir/AGENTS.md" || -e "$repo_dir/CLAUDE.md" ]]; then
  echo "AGENTS.md or CLAUDE.md already exists; refusing to overwrite." >&2
  exit 1
fi

cp "$repo_dir/docs/agent-templates/AGENTS.template.md" "$repo_dir/AGENTS.md"
cp "$repo_dir/docs/agent-templates/CLAUDE.template.md" "$repo_dir/CLAUDE.md"
echo "Installed AGENTS.md and CLAUDE.md"
