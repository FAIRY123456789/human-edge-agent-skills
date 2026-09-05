#!/usr/bin/env bash
set -Eeuo pipefail

ORIGIN="${ORIGIN:-http://127.0.0.1}"
APP_PATH="${APP_PATH:-}"
INTERNAL_API="${INTERNAL_API:-}"
PROTECTED_URLS="${PROTECTED_URLS:-}"
TMP_DIR="$(mktemp -d /tmp/deploy-verify.XXXXXX)"
trap 'rm -rf -- "$TMP_DIR"' EXIT

curl_get() {
    curl --fail --silent --show-error --location --connect-timeout 3 --max-time 15 --retry 2 --retry-delay 1 "$1"
}

base="${ORIGIN}${APP_PATH}"
curl_get "${base}/" >"$TMP_DIR/index.html"
grep -Eqi '<!doctype[[:space:]]+html|<html' "$TMP_DIR/index.html"

asset_path() {
    grep -Eo "${APP_PATH}/assets/[^\"[:space:]]+\\.${1}" "$TMP_DIR/index.html" | head -n1
}

for extension in js css; do
    asset="$(asset_path "$extension")"
    [[ -n "$asset" ]] || { printf 'missing %s asset reference\n' "$extension" >&2; exit 1; }
    curl --fail --silent --show-error --location --connect-timeout 3 --max-time 15 -D "$TMP_DIR/$extension.headers" -o "$TMP_DIR/$extension.body" "${ORIGIN}${asset}"
    if head -c 256 "$TMP_DIR/$extension.body" | grep -Eqi '<!doctype[[:space:]]+html|<html'; then
        printf '%s asset returned HTML\n' "$extension" >&2
        exit 1
    fi
done
grep -Eqi '^content-type:[[:space:]]*(application|text)/(javascript|x-javascript)' "$TMP_DIR/js.headers"
grep -Eqi '^content-type:[[:space:]]*text/css' "$TMP_DIR/css.headers"

if [[ -n "$INTERNAL_API" ]]; then
    curl_get "${INTERNAL_API}/health" >"$TMP_DIR/internal-health.json"
else
    curl_get "${base}/api/health" >"$TMP_DIR/public-health.json"
fi

for protected in $PROTECTED_URLS; do
    curl_get "$protected" >"$TMP_DIR/protected-$(printf '%s' "$protected" | sha256sum | cut -c1-12).body"
    [[ -s "$TMP_DIR/protected-$(printf '%s' "$protected" | sha256sum | cut -c1-12).body" ]]
done

if [[ -n "${VERIFY_HOOK:-}" ]]; then
    "$VERIFY_HOOK"
fi
printf 'VERIFY PASS origin=%s path=%s\n' "$ORIGIN" "${APP_PATH:-/}"
