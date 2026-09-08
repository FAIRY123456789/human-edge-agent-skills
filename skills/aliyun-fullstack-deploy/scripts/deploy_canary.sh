#!/usr/bin/env bash
set -Eeuo pipefail

RELEASE_DIR="${RELEASE_DIR:?set RELEASE_DIR to an extracted release root}"
APP_NAME="${APP_NAME:-app}"
PYTHON_BIN="${PYTHON_BIN:-/usr/bin/python3.11}"
APP_MODULE="${APP_MODULE:-backend.app.main:app}"
CANARY_PORT="${CANARY_PORT:-18001}"
APP_BASE_PATH="${APP_BASE_PATH:-}"
CANARY_HEALTH_PATH="${CANARY_HEALTH_PATH:-${APP_BASE_PATH}/api/health}"
ENV_FILE="${ENV_FILE:-}"
INDEX_URL="${INDEX_URL:-https://pypi.org/simple}"
VENV_SEED="${VENV_SEED:-}"
CANARY_ID="${CANARY_ID:-$(date -u +%Y%m%dT%H%M%SZ)-$$}"
CANARY_ROOT="${CANARY_ROOT:-/opt/${APP_NAME}-canary/$CANARY_ID}"
CANARY_STORAGE="${CANARY_STORAGE:-$CANARY_ROOT/storage}"
VENV_PY="$CANARY_ROOT/.venv/bin/python"
PID_FILE="$CANARY_ROOT/canary.pid"
LOG_FILE="$CANARY_ROOT/canary.log"

[[ -d "$RELEASE_DIR" && -f "$RELEASE_DIR/backend/requirements.txt" ]] || { printf 'invalid release: %s\n' "$RELEASE_DIR" >&2; exit 1; }
[[ -x "$PYTHON_BIN" ]] || { printf 'missing Python: %s\n' "$PYTHON_BIN" >&2; exit 1; }
ss -ltn "sport = :$CANARY_PORT" | grep -q LISTEN && { printf 'port already in use: %s\n' "$CANARY_PORT" >&2; exit 1; }

install -d -m 0755 "$(dirname "$CANARY_ROOT")"
cp -a "$RELEASE_DIR" "$CANARY_ROOT"
install -d -m 0750 "$CANARY_STORAGE"
if [[ -n "$VENV_SEED" ]]; then
    [[ -x "$VENV_SEED/bin/python" ]] || { printf 'invalid VENV_SEED: %s\n' "$VENV_SEED" >&2; exit 1; }
    cp -a "$VENV_SEED" "$CANARY_ROOT/.venv"
    "$VENV_PY" -m pip install --disable-pip-version-check --no-index -r "$CANARY_ROOT/backend/requirements.txt"
    "$VENV_PY" -m pip check
else
    "$PYTHON_BIN" -m venv "$CANARY_ROOT/.venv"
    "$VENV_PY" -m pip install --disable-pip-version-check --prefer-binary --timeout 60 --retries 3 --index-url "$INDEX_URL" -r "$CANARY_ROOT/backend/requirements.txt"
fi

cat >"$CANARY_ROOT/start-canary.sh" <<'SH'
#!/usr/bin/env bash
set -Eeuo pipefail
if [[ -n "${CANARY_ENV_FILE:-}" && -f "$CANARY_ENV_FILE" ]]; then
    set -a
    # The environment file stays on the server and is never printed.
    source "$CANARY_ENV_FILE"
    set +a
fi
export APP_HOST=127.0.0.1 APP_PORT="$CANARY_PORT" APP_BASE_PATH="$CANARY_BASE_PATH" STORAGE_ROOT="$CANARY_STORAGE"
cd "$CANARY_ROOT"
exec "$CANARY_VENV_PY" -m uvicorn "$CANARY_APP_MODULE" --host 127.0.0.1 --port "$CANARY_PORT" --workers 1
SH

CANARY_ENV_FILE="$ENV_FILE" CANARY_PORT="$CANARY_PORT" CANARY_BASE_PATH="$APP_BASE_PATH" CANARY_STORAGE="$CANARY_STORAGE" CANARY_ROOT="$CANARY_ROOT" CANARY_VENV_PY="$VENV_PY" CANARY_APP_MODULE="$APP_MODULE" \
    nohup bash "$CANARY_ROOT/start-canary.sh" >"$LOG_FILE" 2>&1 &
printf '%s\n' "$!" >"$PID_FILE"

health="http://127.0.0.1:${CANARY_PORT}${CANARY_HEALTH_PATH}"
for attempt in {1..30}; do
    if curl --fail --silent --show-error --connect-timeout 2 --max-time 5 "$health" >"$CANARY_ROOT/health.json"; then
        printf 'CANARY PASS root=%s port=%s pid=%s\n' "$CANARY_ROOT" "$CANARY_PORT" "$(<"$PID_FILE")"
        exit 0
    fi
    if ! kill -0 "$(<"$PID_FILE")" 2>/dev/null; then
        tail -n 100 "$LOG_FILE" >&2 || true
        exit 1
    fi
    sleep 1
done
tail -n 100 "$LOG_FILE" >&2 || true
exit 1
