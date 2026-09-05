#!/usr/bin/env bash
set -Eeuo pipefail

RELEASE_DIR="${RELEASE_DIR:?set RELEASE_DIR}"
VERSION="${VERSION:?set VERSION}"
APP_NAME="${APP_NAME:-app}"
APP_ROOT="${APP_ROOT:-/opt/$APP_NAME}"
SERVICE_NAME="${SERVICE_NAME:-$APP_NAME.service}"
SHARED_STORAGE="${SHARED_STORAGE:-$APP_ROOT/storage}"
PYTHON_BIN="${PYTHON_BIN:-/usr/bin/python3.11}"
INDEX_URL="${INDEX_URL:-https://pypi.org/simple}"
VENV_SEED="${VENV_SEED:-}"
WWW_LINK="${WWW_LINK:-}"
HEALTH_URL="${HEALTH_URL:-}"
REUSE_EXISTING_TARGET="${REUSE_EXISTING_TARGET:-0}"
RELEASES_ROOT="$APP_ROOT/releases"
TARGET="$RELEASES_ROOT/$VERSION"
STATE_ROOT="$APP_ROOT/deployment-state"

restore_previous() {
    if [[ -n "$previous" && -d "$previous" ]]; then
        ln -s "$previous" "$APP_ROOT/current.rollback"
        mv -Tf "$APP_ROOT/current.rollback" "$APP_ROOT/current"
        if [[ -n "$WWW_LINK" && -d "$previous/frontend/dist" ]]; then
            ln -s "$previous/frontend/dist" "${WWW_LINK}.rollback"
            mv -Tf "${WWW_LINK}.rollback" "$WWW_LINK"
        fi
    else
        rm -f -- "$APP_ROOT/current"
        if [[ -n "$WWW_LINK" ]]; then
            rm -f -- "$WWW_LINK"
        fi
    fi
    systemctl restart "$SERVICE_NAME" || true
}

[[ "${EUID}" -eq 0 ]] || { printf 'run as root\n' >&2; exit 1; }
[[ -d "$RELEASE_DIR" ]] || { printf 'release missing: %s\n' "$RELEASE_DIR" >&2; exit 1; }
systemctl cat "$SERVICE_NAME" | grep -Fq "$APP_ROOT/current" || { printf 'service is not current-symlink aware; install a validated unit first\n' >&2; exit 1; }
install -d -m 0755 "$RELEASES_ROOT" "$STATE_ROOT"
install -d -m 0750 "$SHARED_STORAGE"
if [[ -e "$TARGET" ]]; then
    [[ "$REUSE_EXISTING_TARGET" == 1 ]] || { printf 'target release already exists: %s\n' "$TARGET" >&2; exit 1; }
    [[ -L "$TARGET/storage" && "$(readlink -f "$TARGET/storage")" == "$(readlink -f "$SHARED_STORAGE")" ]] || { printf 'existing target storage link is invalid\n' >&2; exit 1; }
    (cd "$TARGET" && sha256sum -c checksums.sha256 >/dev/null)
    "$TARGET/.venv/bin/python" -m pip install --disable-pip-version-check --no-index -r "$TARGET/backend/requirements.txt"
    "$TARGET/.venv/bin/python" -m pip check
else
    cp -a "$RELEASE_DIR" "$TARGET"
    ln -s "$SHARED_STORAGE" "$TARGET/storage"
    if [[ -n "$VENV_SEED" ]]; then
        [[ -x "$VENV_SEED/bin/python" ]] || { printf 'invalid VENV_SEED: %s\n' "$VENV_SEED" >&2; exit 1; }
        cp -a "$VENV_SEED" "$TARGET/.venv"
        "$TARGET/.venv/bin/python" -m pip install --disable-pip-version-check --no-index -r "$TARGET/backend/requirements.txt"
        "$TARGET/.venv/bin/python" -m pip check
    else
        "$PYTHON_BIN" -m venv "$TARGET/.venv"
        "$TARGET/.venv/bin/python" -m pip install --disable-pip-version-check --prefer-binary --timeout 60 --retries 3 --index-url "$INDEX_URL" -r "$TARGET/backend/requirements.txt"
    fi
fi

if [[ "$REUSE_EXISTING_TARGET" == 1 && -L "$APP_ROOT/current" && "$(readlink -f "$APP_ROOT/current")" == "$TARGET" ]]; then
    [[ -z "$WWW_LINK" || "$(readlink -f "$WWW_LINK")" == "$TARGET/frontend/dist" ]] || { printf 'active static link does not match target\n' >&2; exit 1; }
    systemctl is-active --quiet "$SERVICE_NAME"
    [[ -z "$HEALTH_URL" ]] || curl --fail --silent --show-error --connect-timeout 2 --max-time 5 "$HEALTH_URL" >/dev/null
    printf 'PROMOTE NOOP PASS version=%s target=%s\n' "$VERSION" "$TARGET"
    exit 0
fi

previous=""
if [[ -L "$APP_ROOT/current" ]]; then
    previous="$(readlink -f "$APP_ROOT/current")"
fi
printf '%s\n' "$previous" >"$STATE_ROOT/previous-release"
printf '%s\n' "$TARGET" >"$STATE_ROOT/pending-release"
ln -s "releases/$VERSION" "$APP_ROOT/current.new"
mv -Tf "$APP_ROOT/current.new" "$APP_ROOT/current"
if [[ -n "$WWW_LINK" ]]; then
    install -d -m 0755 "$(dirname "$WWW_LINK")"
    ln -s "$TARGET/frontend/dist" "${WWW_LINK}.new"
    mv -Tf "${WWW_LINK}.new" "$WWW_LINK"
fi

systemctl restart "$SERVICE_NAME"
systemctl is-active --quiet "$SERVICE_NAME" || {
    restore_previous
    exit 1
}
if [[ -n "$HEALTH_URL" ]]; then
    ready=0
    for attempt in {1..30}; do
        if curl --fail --silent --show-error --connect-timeout 2 --max-time 5 "$HEALTH_URL" >/dev/null; then
            ready=1
            break
        fi
        sleep 1
    done
    [[ "$ready" -eq 1 ]] || {
        restore_previous
        printf 'health check failed after promotion: %s\n' "$HEALTH_URL" >&2
        exit 1
    }
fi
mv "$STATE_ROOT/pending-release" "$STATE_ROOT/active-release"
printf 'PROMOTE PASS version=%s previous=%s\n' "$VERSION" "${previous:-none}"
