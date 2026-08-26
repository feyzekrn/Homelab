# 🐧 Linux

[← Back to Dev PC](../README.md)

> 🔜 **Planned.** There is no Linux dev machine yet, so there is no tested setup here.

The homelab is operated from a Mac. This folder exists so the structure is already in place if that changes — a second workstation, or a Linux VM used for development.

---

## What Would Carry Over

Most of it. The two parts that are OS-independent are the interesting ones:

| | Portable? |
|---|---|
| [`starship.toml`](../starship/starship.toml) | ✅ Unchanged — the same file already runs on the Debian and Ubuntu hosts |
| [`zshrc`](../starship/zshrc) | ⚠️ Mostly — the Homebrew paths for the two zsh add-ons would become distribution paths |
| [`gen.py`](../starship/gen.py) | ✅ Unchanged — `fontmap.py` already searches Linux font directories |
| `bootstrap.sh` | ❌ macOS-specific — Homebrew, `sed -i ''`, the Warp settings path |

The prompt itself is a solved problem on Linux; [servers/bootstrap.sh](../servers/bootstrap.sh) already installs it on Debian and Ubuntu today. What is missing is the workstation layer: package installation, a terminal emulator and the font.

## What Would Have To Be Decided

**Package manager.** `apt`, `dnf` and `pacman` name these packages differently, and `zsh-autosuggestions` is not in every default repository. Homebrew on Linux would keep one code path but is a heavy answer for three packages.

**Terminal.** Warp has a Linux build, which would keep the setup identical. Alacritty, Kitty and WezTerm are the alternatives — all of them fine with Nerd Fonts, none of them with Warp's block model.

**Font.** No cask equivalent. The JetBrains Mono Nerd Font release from [ryanoasis/nerd-fonts](https://github.com/ryanoasis/nerd-fonts) unpacked into `~/.local/share/fonts/`, followed by `fc-cache -f`.

---

Until a real machine exists to test it on, this stays a plan. An untested setup script is worse than none.
