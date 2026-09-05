#!/usr/bin/env bash
set -Eeuo pipefail

APP_NAME="${APP_NAME:-app}"
APP_ROOT="${APP_ROOT:-/opt/$APP_NAME}"
SERVICE_NAME="${SERVICE_NAME:-$APP_NAME.service}"
WWW_LINK="${WWW_LINK:-}"
HEALTH_URL="${HEALTH_URL:-}"
STATE_ROOT="$APP_ROOT/deployment-state"
PREVIOUS_FILE="$STATE_ROOT/previous-release"

[[ "${EUID}" -eq 0 ]] || { printf 'run as root\n' >&2; exit 1; }
[[ -f "$PREVIOUS_FILE" ]] || { printf 'previous release metadata missing\n' >&2; exit 1; }
previous="$(<"$PREVIOUS_FILE")"
[[ -n "$previous" && -d "$previous" ]] || { printf 'previous release unavailable: %s\n' "$previous" >&2; exit 1; }
current="$(readlink -f "$APP_ROOT/current" || true)"
ln -s "$previous" "$APP_ROOT/current.rollback"
mv -Tf "$APP_ROOT/current.rollback" "$APP_ROOT/current"
if [[ -n "$WWW_LINK" && -d "$previous/frontend/dist" ]]; then
    ln -s "$previous/frontend/dist" "${WWW_LINK}.rollback"
    mv -Tf "${WWW_LINK}.rollback" "$WWW_LINK"
fi
systemctl restart "$SERVICE_NAME"
systemctl is-active --quiet "$SERVICE_NAME"
if [[ -n "$HEALTH_URL" ]]; then
    ready=0
    for attempt in {1..30}; do
        if curl --fail --silent --show-error --connect-timeout 2 --max-time 5 "$HEALTH_URL" >/dev/null; then
            ready=1
            break
        fi
        sleep 1
    done
    [[ "$ready" -eq 1 ]] || { printf 'rollback health check failed: %s\n' "$HEALTH_URL" >&2; exit 1; }
fi
printf '%s\n' "$current" >"$STATE_ROOT/rolled-back-from"
printf 'ROLLBACK PASS current=%s from=%s\n' "$previous" "${current:-unknown}"
