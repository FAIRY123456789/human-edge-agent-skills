#!/usr/bin/env bash
set -Eeuo pipefail

APP_NAME="${APP_NAME:-app}"
APP_ROOT="${APP_ROOT:-/opt/$APP_NAME}"
WWW_ROOT="${WWW_ROOT:-/var/www/$APP_NAME}"
SERVICE_NAME="${SERVICE_NAME:-$APP_NAME.service}"
ENV_FILE="${ENV_FILE:-$APP_ROOT/.env}"
PYTHON_BIN="${PYTHON_BIN:-}"
PROTECTED_PATHS="${PROTECTED_PATHS:-}"

section() { printf '\n## %s\n' "$1"; }
run_optional() { printf '$ %s\n' "$*"; "$@" 2>&1 || printf '[command unavailable or returned non-zero]\n'; }

section identity
run_optional id
run_optional hostnamectl
run_optional uname -a

section resources
run_optional nproc
run_optional free -h
run_optional df -hT
run_optional df -ih

section security
run_optional getenforce
run_optional sestatus
run_optional firewall-cmd --state
run_optional systemctl is-active firewalld

section runtimes
if [[ -n "$PYTHON_BIN" ]]; then
    run_optional "$PYTHON_BIN" --version
fi
run_optional python3 --version
run_optional node --version
run_optional npm --version
run_optional java -version
run_optional nginx -v
run_optional systemctl --version
run_optional ssh -V

section package-managers
for command_name in dnf yum apt-get zypper; do
    command -v "$command_name" 2>/dev/null || true
done

section listeners
run_optional ss -lntup

section application
run_optional ls -ld "$APP_ROOT" "$WWW_ROOT"
for protected_path in $PROTECTED_PATHS; do
    run_optional ls -ld "$protected_path"
done
run_optional find "$APP_ROOT" -maxdepth 2 -mindepth 1 -printf '%M %u:%g %s %TY-%Tm-%TdT%TH:%TM:%TS %p\n'
run_optional systemctl status "$SERVICE_NAME" --no-pager
run_optional systemctl cat "$SERVICE_NAME"

section environment-status
if [[ -f "$ENV_FILE" ]]; then
    stat -c '%A %U:%G %s %n' "$ENV_FILE"
    awk -F= '/^[A-Za-z_][A-Za-z0-9_]*=/{value=$0; sub(/^[^=]*=/,"",value); printf "%s=%s\n",$1,(length(value)>0?"configured":"empty")}' "$ENV_FILE"
else
    printf 'environment file missing: %s\n' "$ENV_FILE"
fi

section nginx-effective-config
run_optional nginx -T

section backups-and-logs
run_optional ls -ld "/opt/${APP_NAME}-backups" /var/backups
run_optional journalctl -u "$SERVICE_NAME" -n 100 --no-pager
