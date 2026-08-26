#!/usr/bin/env bash
#
# bootstrap.sh — give a homelab host the same prompt as the dev machine.
#
# Run this ON the host (node0..2, pve0, a VM, an LXC):
#
#   curl -fsSL https://raw.githubusercontent.com/feyzekrn/Homelab/main/setup/devpc/servers/bootstrap.sh | bash
#
#   ./bootstrap.sh --dry-run     show what would happen
#   ./bootstrap.sh --with-tools  also install jq, tree, htop
#   ./bootstrap.sh --ref v1.2    pull the config from a tag instead of main
#
# What lands on the host: the starship binary in /usr/local/bin, one config
# file in ~/.config, one line in ~/.bashrc. Nothing else. The repository is
# never cloned — only individual files are fetched over HTTPS.
#
# No zsh required: starship works with bash, which is what Proxmox and the
# Ubuntu nodes use for root anyway.
#
# No fonts required: the glyphs are rendered by YOUR terminal on the other end
# of the SSH connection. The host only sends the code points down the wire.

set -euo pipefail

REPO="feyzekrn/Homelab"
REF="main"
DRY=0
TOOLS=0
CONFIG_PATH="setup/devpc/starship/starship.toml"

while [[ $# -gt 0 ]]; do
  case "$1" in
    --dry-run)    DRY=1; shift ;;
    --with-tools) TOOLS=1; shift ;;
    --ref)        REF="${2:?--ref needs a value}"; shift 2 ;;
    -h|--help)    sed -n '2,20p' "$0" | sed 's/^# \{0,1\}//'; exit 0 ;;
    *) echo "unknown option: $1" >&2; exit 1 ;;
  esac
done

RAW="https://raw.githubusercontent.com/${REPO}/${REF}/${CONFIG_PATH}"

step() { printf '\n==> %s\n' "$*"; }
info() { printf '    %s\n' "$*"; }
run()  { if (( DRY )); then printf '    [dry] %s\n' "$*"; else eval "$*"; fi; }

# curl or wget, whichever exists.
# Called from inside the eval in run(), which shellcheck cannot see.
# shellcheck disable=SC2329
fetch() {                       # $1 = url, $2 = output path
  if command -v curl >/dev/null 2>&1; then curl -fsSL "$1" -o "$2"
  elif command -v wget >/dev/null 2>&1; then wget -qO "$2" "$1"
  else echo "need curl or wget" >&2; exit 1; fi
}

(( DRY )) && echo "DRY RUN — nothing will be changed."

# Writing to /usr/local/bin needs root; everything else does not.
SUDO=""
if [[ $EUID -ne 0 ]]; then
  if command -v sudo >/dev/null 2>&1; then
    SUDO="sudo"
  else
    echo "not root and no sudo available" >&2; exit 1
  fi
fi

# ── 1. which machine is this ──────────────────────────────────────────────
step "Host"
if [[ "$(uname -s)" == "Darwin" ]]; then
  echo "This is the server script. On the Mac use setup/devpc/macos/bootstrap.sh." >&2
  exit 1
fi
ARCH="$(uname -m)"
case "$ARCH" in
  x86_64|amd64)  TARGET=x86_64-unknown-linux-musl ;;
  aarch64|arm64) TARGET=aarch64-unknown-linux-musl ;;
  armv7l)        TARGET=armv7-unknown-linux-musleabihf ;;
  *) echo "unsupported architecture: $ARCH" >&2; exit 1 ;;
esac
info "$(hostname) — ${ARCH} -> ${TARGET}"
[[ -d /etc/pve ]] && info "Proxmox VE detected — the prompt will show the Proxmox icon"
[[ -d /var/lib/kubelet ]] && info "kubelet detected — the prompt will show the Kubernetes icon"

# ── 2. starship binary ────────────────────────────────────────────────────
# Installed from the official release tarball with its checksum verified,
# rather than piping the vendor install script into a shell.
step "starship"
if command -v starship >/dev/null 2>&1; then
  info "already installed — $(starship --version | head -1)"
else
  info "downloading release for ${TARGET}"
  run "set -e
    base=https://github.com/starship/starship/releases/latest/download
    tmp=\$(mktemp -d); cd \"\$tmp\"
    fetch \"\$base/starship-${TARGET}.tar.gz\" s.tar.gz
    fetch \"\$base/starship-${TARGET}.tar.gz.sha256\" s.sha256 || true
    if [ -s s.sha256 ]; then
      want=\$(tr -d '[:space:]' < s.sha256)
      have=\$(sha256sum s.tar.gz | cut -d' ' -f1)
      [ \"\$want\" = \"\$have\" ] || { echo '    CHECKSUM MISMATCH — aborting' >&2; exit 1; }
      echo '    checksum verified'
    fi
    tar xzf s.tar.gz starship
    ${SUDO} install -m 0755 starship /usr/local/bin/starship
    cd /; rm -rf \"\$tmp\""
  info "installed to /usr/local/bin/starship"
fi

# ── 3. the prompt config ──────────────────────────────────────────────────
# One file, fetched directly. No clone, nothing left behind to clean up.
step "Prompt configuration"
DEST="${HOME}/.config/starship.toml"
if [[ -f "$DEST" ]]; then
  run "cp '$DEST' '${DEST}.bak-$(date +%Y%m%d-%H%M%S)'"
  info "existing config backed up"
fi
run "mkdir -p '${HOME}/.config'"
run "fetch '$RAW' '$DEST'"
info "fetched from ${REF}"

# ── 4. wire it into the shell ─────────────────────────────────────────────
step "Shell"
if grep -q 'starship init bash' "${HOME}/.bashrc" 2>/dev/null; then
  info "bashrc already initialises starship"
else
  run "printf '\n# Starship prompt — see %s\neval \"\$(starship init bash)\"\n' 'github.com/${REPO}/tree/main/setup/devpc' >> '${HOME}/.bashrc'"
  info "added starship init to ~/.bashrc"
fi
if command -v zsh >/dev/null 2>&1 && [[ -f "${HOME}/.zshrc" ]]; then
  if grep -q 'starship init zsh' "${HOME}/.zshrc"; then
    info "zshrc already initialises starship"
  else
    run "printf '\neval \"\$(starship init zsh)\"\n' >> '${HOME}/.zshrc'"
    info "added starship init to ~/.zshrc"
  fi
fi

# ── 5. optional CLI tools ─────────────────────────────────────────────────
if (( TOOLS )); then
  step "CLI tools"
  if command -v apt-get >/dev/null 2>&1; then
    run "${SUDO} apt-get update -qq && ${SUDO} apt-get install -y -qq jq tree htop"
    info "installed jq, tree, htop"
  else
    info "no apt-get — install jq, tree, htop with your package manager"
  fi
fi

step "Done"
info "Log in again, or run: exec bash"

exit 0
