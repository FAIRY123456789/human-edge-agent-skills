#!/usr/bin/env bash
set -Eeuo pipefail

PYTHON_BIN="${PYTHON_BIN:-/usr/bin/python3.11}"
EXPECTED_PYTHON="${EXPECTED_PYTHON:-3.11}"
APP_ROOT="${APP_ROOT:-/opt/app}"
VENV_PY="${VENV_PY:-$APP_ROOT/.venv/bin/python}"
REQUIREMENTS="${REQUIREMENTS:-$APP_ROOT/backend/requirements.txt}"

[[ -x "$PYTHON_BIN" ]] || { printf 'missing interpreter: %s\n' "$PYTHON_BIN" >&2; exit 1; }
"$PYTHON_BIN" - "$EXPECTED_PYTHON" <<'PY'
import platform, sys
expected = tuple(map(int, sys.argv[1].split(".")))
print(sys.executable)
print(platform.platform())
print(sys.version)
assert sys.version_info[:2] == expected, (sys.version_info[:2], expected)
PY

if [[ -x "$VENV_PY" ]]; then
    "$VENV_PY" - "$EXPECTED_PYTHON" <<'PY'
import sys
expected = tuple(map(int, sys.argv[1].split(".")))
print(sys.executable)
print(sys.version)
assert sys.version_info[:2] == expected, (sys.version_info[:2], expected)
PY
    "$VENV_PY" -m pip --version
else
    printf 'venv missing: %s\n' "$VENV_PY"
fi

[[ -f "$REQUIREMENTS" ]] || { printf 'requirements missing: %s\n' "$REQUIREMENTS" >&2; exit 1; }
if grep -Eq '(^|[<>=[:space:]])fastapi([<>=[:space:]]|$)' "$REQUIREMENTS"; then
    printf 'FastAPI requirement present. Probe indexes before installation with:\n'
    printf '  %s -m pip index versions fastapi --index-url <index-url> --timeout 20\n' "$PYTHON_BIN"
fi
