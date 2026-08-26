# 🍎 macOS

[← Back to Dev PC](../README.md)

The dev machine is a Mac, so this is the only OS with a real setup rather than a plan. Everything here is driven by one script.

---

## bootstrap.sh

```bash
./bootstrap.sh              # install and configure
./bootstrap.sh --dry-run    # print what would happen, change nothing
./bootstrap.sh --no-apps    # tooling only, skip Warp
./bootstrap.sh --help
```

Without a clone:

```bash
curl -fsSL https://raw.githubusercontent.com/feyzekrn/Homelab/main/setup/devpc/macos/bootstrap.sh | bash
```

### What it does, in order

| Step | Action | Skipped when |
|---|---|---|
| 1 | Install Homebrew | `brew` is on the PATH |
| 2 | `starship`, `zsh-autosuggestions`, `zsh-syntax-highlighting`, `jq` | already installed |
| 3 | `font-jetbrains-mono-nerd-font` | already installed |
| 4 | Warp | already installed, or `--no-apps` |
| 5 | Write `~/.zshrc` and `~/.config/starship.toml` | never — but the originals are backed up |
| 6 | Switch Warp's font to the non-Mono variant | already set, or Warp is running |

### Two modes for the config files

The script figures out where to read `zshrc` and `starship.toml` from:

- **local** — it found `../starship/` next to itself, so it is running from a clone and copies from there
- **remote** — it was piped from `curl` and has no siblings, so it fetches from `raw.githubusercontent.com`

The mode is printed during the run, so there is never a question which files were used.

### What it will not do

**It never runs `sudo` on its own.** The single privileged step is Homebrew's own installer, which asks for your password to create `/opt/homebrew`. Everything after that is user-level.

**It does not touch Warp's settings while Warp is running.** Warp owns `~/.warp/settings.toml` and rewrites it from memory, so an edit made underneath it is lost on the next save. If Warp is open the script says so and prints the UI path instead.

### Backups

Every file that would be replaced is copied to `~/.dotfiles-backup/<timestamp>/` first. Restoring is a `cp` back — see [commands.md](../commands.md#g-undoing-it).

---

## What Ends Up Where

| Path | Content |
|---|---|
| `~/.zshrc` | Shell configuration — history, completion, plugins, aliases |
| `~/.config/starship.toml` | The prompt |
| `~/.zprofile` | Homebrew on the PATH (only touched if the line is missing) |
| `~/.warp/settings.toml` | Font name only |
| `~/.dotfiles-backup/` | Whatever was there before |

The sources for the first two live in [starship](../starship) and are the same files that go onto the servers.

---

## The zsh Configuration

`~/.zshrc` is around 60 lines and does five things: history, completion, key bindings, aliases, and loading the three add-ons. No framework — the reasoning is in [terminal-designs.md](../terminal-designs.md#what-it-replaced-and-why).

Worth knowing about, because they are not defaults:

| | |
|---|---|
| `SHARE_HISTORY` | History is shared live between open tabs |
| `HIST_IGNORE_SPACE` | A command typed with a leading space is not recorded |
| `AUTO_CD` | `Projects` instead of `cd Projects` |
| **↑ / ↓** | Filters history by what you have already typed, instead of walking through everything |
| `json` | `jq` wrapper — works on a file, a pipe, or with a filter argument |
| `jsonclip` | Formats the clipboard and copies it back |

```bash
curl -s https://api.example.com/things | json     # pretty-print a response
json '.items[] | .name' data.json                 # filter a file
```

Load order matters at the end of the file: `zsh-syntax-highlighting` has to be sourced **last**, otherwise it does not see the widgets the other add-ons define.
