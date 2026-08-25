#!/usr/bin/env bash
set -euo pipefail

script_dir="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
project_dir="$(cd -- "$script_dir/.." && pwd)"
if [[ -n "${SINEW_BUILD_DIR:-}" ]]; then
  build_dir="$SINEW_BUILD_DIR"
  mkdir -p "$build_dir"
else
  build_dir="$(mktemp -d "${TMPDIR:-/tmp}/sinew-styles.XXXXXX")"
fi

colors=(origami paper high-contrast blueprint scholar unmasked the-give the-meeting movement)

python3 "$script_dir/validate.py"
python3 "$script_dir/check_contrast.py"
for color in "${colors[@]}"; do
  output_dir="$build_dir/$color"
  echo "Rendering color-${color}"
  quarto render "$project_dir" \
    --profile "color-${color}" \
    --output-dir "$output_dir" \
    --quiet
  python3 "$script_dir/check_render.py" \
    "$output_dir/index.html" "$color"
done

echo "Rendered 9 styles under $build_dir"
