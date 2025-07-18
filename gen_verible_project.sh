#!/bin/bash

# Generate .verible-project with all relevant include dirs
echo "Generating .verible-project..."

# Delete old one if it exists
rm -f .verible-project

# Find all unique directories containing .sv or .v files (excluding common build folders)
find . \
  -type f \( -name "*.sv" -o -name "*.v" \) \
  -not -path "./.*" \
  -not -path "*/build/*" \
  -not -path "*/out/*" \
  -exec dirname {} \; \
  | sort -u \
  | sed 's|^./|--include_dir=|' \
  > .verible-project

echo "Done. Created .verible-project with these entries:"
cat .verible-project

