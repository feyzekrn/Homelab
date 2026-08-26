#!/usr/bin/env bash
#
# bootstrap.sh — set up the macOS dev machine in one run.
#
#   ./bootstrap.sh              install and configure
#   ./bootstrap.sh --dry-run    show what would happen, change nothing
#   ./bootstrap.sh --no-apps    skip the GUI apps (Warp), tooling only
#
# Or without a clone:
#   curl -fsSL https://raw.githubusercontent.com/feyzekrn/Homelab/main/setup/devpc/macos/bootstrap.sh | bash
#
# Safe to run repeatedly. Anything already installed is skipped, and every file
# this script would overwrite is copied to ~/.dotfiles-backup/<timestamp>/ first.
#
# The only step that asks for your password is the Homebrew installer itself —
# it needs sudo to create /opt/homebrew. Nothing here runs sudo on its own.

set -euo pipefail

RAW_BASE="https://raw.githubusercontent.com/feyzekrn/Homelab/main/setup/devpc/starship"
BACKUP_DIR="${HOME}/.dotfiles-backup/$(date +%Y%m%d-%H%M%S)"
DRY=0
APPS=1
TILDE="~"          # for shortening paths in output

FORMULAE=(starship zsh-autosuggestions zsh-syntax-highlighting jq)
CASKS=(font-jetbrains-mono-nerd-font)
APP_CASKS=(warp)

for arg in "$@"; do
  case "$arg" in
    --dry-run) DRY=1 ;;
    --no-apps) APPS=0 ;;
    -h|--help) sed -n '2,18p' "$0" | sed 's/^# \{0,1\}//'; exit 0 ;;
    *) echo "unknown option: $arg" >&2; exit 1 ;;
  esac
done

# ── output helpers ────────────────────────────────────────────────────────
bold() { printf '\033[1m%s\033[0m\n' "$*"; }
step() { printf '\n\033[1;36m==>\033[0m \033[1m%s\033[0m\n' "$*"; }
info() { printf '    %s\n' "$*"; }
skip() { printf '    \033[2m%s\033[0m\n' "$*"; }
warn() { printf '    \033[33m%s\033[0m\n' "$*"; }
run()  { if (( DRY )); then printf '    \033[2m[dry] %s\033[0m\n' "$*"; else eval "$*"; fi; }

(( DRY )) && bold "DRY RUN — nothing will be changed."

# ── 0. sanity ─────────────────────────────────────────────────────────────
[[ "$(uname -s)" == "Darwin" ]] || { echo "This script is for macOS. See ../linux or ../windows." >&2; exit 1; }

# Where do the config files come from: this clone, or GitHub?
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd 2>/dev/null || echo "")"
LOCAL_SRC="${SCRIPT_DIR}/../starship"
if [[ -n "$SCRIPT_DIR" && -f "${LOCAL_SRC}/starship.toml" ]]; then
  SOURCE_MODE="local"
else
  SOURCE_MODE="remote"
fi

# ── 1. Homebrew ───────────────────────────────────────────────────────────
step "Homebrew"
if command -v brew >/dev/null 2>&1; then
  skip "already installed — $(brew --version | head -1)"
else
  info "not found, installing (this will ask for your password)"
  # Single quotes on purpose: the $(curl ...) must be evaluated by the inner
  # bash that Homebrew's installer runs in, not expanded here.
  # shellcheck disable=SC2016
  run '/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"'
  # Apple Silicon puts brew outside the default PATH
  if [[ -x /opt/homebrew/bin/brew ]]; then
    eval "$(/opt/homebrew/bin/brew shellenv)"
    if ! grep -q 'brew shellenv' "${HOME}/.zprofile" 2>/dev/null; then
      run "printf '\neval \"\$(/opt/homebrew/bin/brew shellenv)\"\n' >> '${HOME}/.zprofile'"
      info "added brew to ~/.zprofile"
    fi
  fi
fi

# ── 2. command line tools ─────────────────────────────────────────────────
step "Command line tools"
for f in "${FORMULAE[@]}"; do
  if brew list --formula "$f" >/dev/null 2>&1; then
    skip "$f — already installed"
  else
    info "installing $f"
    run "brew install $f"
  fi
done

# ── 3. font ───────────────────────────────────────────────────────────────
# The prompt uses Nerd Font glyphs. Without this font every icon is a box.
step "Nerd Font"
for c in "${CASKS[@]}"; do
  if brew list --cask "$c" >/dev/null 2>&1; then
    skip "$c — already installed"
  else
    info "installing $c"
    run "brew install --cask $c"
  fi
done

# ── 4. terminal ───────────────────────────────────────────────────────────
if (( APPS )); then
  step "Terminal"
  for c in "${APP_CASKS[@]}"; do
    if brew list --cask "$c" >/dev/null 2>&1 || [[ -d "/Applications/Warp.app" ]]; then
      skip "$c — already installed"
    else
      info "installing $c"
      run "brew install --cask $c"
    fi
  done
else
  step "Terminal"; skip "skipped (--no-apps)"
fi

# ── 5. shell + prompt config ──────────────────────────────────────────────
step "Shell and prompt configuration"

backup_then_write() {          # $1 = destination, $2 = source name in starship/
  local dest="$1" name="$2"
  if [[ -f "$dest" ]]; then
    run "mkdir -p '$BACKUP_DIR' && cp '$dest' '$BACKUP_DIR/'"
    info "backed up $(basename "$dest") -> ${BACKUP_DIR/#$HOME/$TILDE}"
  fi
  run "mkdir -p '$(dirname "$dest")'"
  if [[ "$SOURCE_MODE" == "local" ]]; then
    run "cp '${LOCAL_SRC}/${name}' '$dest'"
  else
    run "curl -fsSL '${RAW_BASE}/${name}' -o '$dest'"
  fi
  info "wrote ${dest/#$HOME/$TILDE}"
}

info "config source: $SOURCE_MODE"
backup_then_write "${HOME}/.zshrc"                 "zshrc"
backup_then_write "${HOME}/.config/starship.toml"  "starship.toml"

# ── 6. Warp font ──────────────────────────────────────────────────────────
# The "Mono" variant squeezes every glyph into one cell, which makes the icons
# look cramped. The regular variant lets them use their natural width.
step "Warp font"
WARP_SETTINGS="${HOME}/.warp/settings.toml"
if [[ ! -f "$WARP_SETTINGS" ]]; then
  warn "no Warp settings yet — start Warp once, then re-run this script"
elif pgrep -x Warp >/dev/null 2>&1; then
  warn "Warp is running and would overwrite the file."
  warn "Set it manually: Settings > Appearance > Text > Font > JetBrainsMono Nerd Font"
elif grep -q 'font_name = "JetBrainsMono Nerd Font"' "$WARP_SETTINGS"; then
  skip "already set to the non-Mono variant"
else
  run "cp '$WARP_SETTINGS' '$BACKUP_DIR/warp-settings.toml' 2>/dev/null || true"
  run "sed -i '' 's/font_name = \"JetBrainsMono Nerd Font Mono\"/font_name = \"JetBrainsMono Nerd Font\"/' '$WARP_SETTINGS'"
  info "switched to the non-Mono variant (bigger icons)"
fi

# ── done ──────────────────────────────────────────────────────────────────
step "Done"
if (( DRY )); then
  info "dry run — nothing was changed."
else
  info "Open a new Warp tab to see the prompt."
  if [[ -d "$BACKUP_DIR" ]]; then
    info "Replaced files are in ${BACKUP_DIR/#$HOME/$TILDE}"
  fi
fi

# Explicit: under `set -e` a trailing `[[ ... ]] && ...` that evaluates false
# would make a fully successful run exit non-zero.
exit 0
