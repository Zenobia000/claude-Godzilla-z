#!/usr/bin/env bash

# Linux entry point. Keep behavior identical to statusline.sh so projects can
# select either filename without maintaining two copies of the formatter.

set -f

script_dir=$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)
exec bash "$script_dir/statusline.sh"
