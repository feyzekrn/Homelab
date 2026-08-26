#!/usr/bin/env bash
#
# deploy.sh — roll the prompt out to several hosts at once, from the dev machine.
#
#   ./deploy.sh root@pve0
#   ./deploy.sh root@node0 root@node1 root@node2
#   ./deploy.sh --with-tools root@pve0
#   ./deploy.sh --dry-run root@pve0
#
# This does not reimplement the installation. It pipes bootstrap.sh into the
# remote shell and lets that script do the work, so there is exactly one
# installation path to maintain and to reason about.
#
# Requirements: key-based SSH to each host (ssh-copy-id <host>), and outbound
# HTTPS from the host — the starship release and the config come from GitHub.

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
BOOTSTRAP="${SCRIPT_DIR}/bootstrap.sh"
REMOTE_ARGS=()
HOSTS=()

while [[ $# -gt 0 ]]; do
  case "$1" in
    --dry-run|--with-tools) REMOTE_ARGS+=("$1"); shift ;;
    --ref) REMOTE_ARGS+=("$1" "${2:?--ref needs a value}"); shift 2 ;;
    -h|--help) sed -n '2,16p' "$0" | sed 's/^# \{0,1\}//'; exit 0 ;;
    -*) echo "unknown option: $1" >&2; exit 1 ;;
    *) HOSTS+=("$1"); shift ;;
  esac
done

[[ -f "$BOOTSTRAP" ]] || { echo "bootstrap.sh not found next to this script" >&2; exit 1; }
[[ ${#HOSTS[@]} -gt 0 ]] || { sed -n '2,16p' "$0" | sed 's/^# \{0,1\}//'; exit 1; }

failed=()
for host in "${HOSTS[@]}"; do
  printf '\n\033[1;36m######\033[0m \033[1m%s\033[0m\n' "$host"

  if ! ssh -o BatchMode=yes -o ConnectTimeout=5 "$host" true 2>/dev/null; then
    printf '    \033[31mno key-based SSH connection. Run: ssh-copy-id %s\033[0m\n' "$host"
    failed+=("$host"); continue
  fi

  if ssh -o BatchMode=yes "$host" bash -s -- "${REMOTE_ARGS[@]}" < "$BOOTSTRAP"; then
    :
  else
    printf '    \033[31mbootstrap failed on %s\033[0m\n' "$host"
    failed+=("$host")
  fi
done

echo
if [[ ${#failed[@]} -eq 0 ]]; then
  echo "All ${#HOSTS[@]} host(s) done. Log in again to see the prompt."
else
  echo "Failed on: ${failed[*]}"
  exit 1
fi
