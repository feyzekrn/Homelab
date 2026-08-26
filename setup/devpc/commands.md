# 📋 Command List — Step by Step

[← Back to Dev PC](./README.md)

![AI-assisted](https://img.shields.io/badge/AI--assisted-Claude-8A63D2?style=flat-square)

Copy-paste order for setting up a machine. Nothing here needs the other documents — the *why* is in [terminal-designs.md](./terminal-designs.md), this page is only the *what*.

Every script is safe to run twice and every one of them takes `--dry-run`.

---

## A. Fresh Mac — The Short Way

One command. It installs Homebrew if missing, then the tooling, the font, Warp, and writes the shell and prompt configuration.

```bash
curl -fsSL https://raw.githubusercontent.com/feyzekrn/Homelab/main/setup/devpc/macos/bootstrap.sh | bash
```

Then:

1. Open Warp.
2. Check **Settings → Appearance → Text → Font** shows `JetBrainsMono Nerd Font` (without *Mono*). The script sets this, but only if Warp was closed while it ran.
3. Open a new tab. The prompt should be there.

> The Homebrew installer asks for your password. That is the only step that needs it — nothing else in the script uses `sudo`.

---

## B. Fresh Mac — Step By Step

Same result, one step at a time, for when you want to see what happens.

**1. Xcode command line tools** (Homebrew needs a compiler)

```bash
xcode-select --install
```

**2. Homebrew**

```bash
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
```

**3. Put brew on the PATH** (Apple Silicon only — the installer prints this too)

```bash
echo 'eval "$(/opt/homebrew/bin/brew shellenv)"' >> ~/.zprofile
eval "$(/opt/homebrew/bin/brew shellenv)"
```

**4. Command line tools**

```bash
brew install starship zsh-autosuggestions zsh-syntax-highlighting jq
```

**5. Font and terminal**

```bash
brew install --cask font-jetbrains-mono-nerd-font
brew install --cask warp
```

**6. Get the repository**

```bash
git clone https://github.com/feyzekrn/Homelab.git ~/Projects/Homelab
cd ~/Projects/Homelab/setup/devpc
```

**7. Look before you leap**

```bash
./macos/bootstrap.sh --dry-run
```

**8. Apply**

```bash
./macos/bootstrap.sh
```

**9. Set the Warp font**

Settings → Appearance → Text → Font → `JetBrainsMono Nerd Font`

**10. New tab.**

---

## C. Existing Mac — Configuration Only

Skip the installs, just take the shell and prompt config. The originals are backed up to `~/.dotfiles-backup/<timestamp>/`.

```bash
cd ~/Projects/Homelab/setup/devpc
./macos/bootstrap.sh --no-apps --dry-run
./macos/bootstrap.sh --no-apps
```

Or by hand, without the script:

```bash
cp setup/devpc/starship/zshrc         ~/.zshrc
cp setup/devpc/starship/starship.toml ~/.config/starship.toml
exec zsh
```

---

## D. Servers And Proxmox

### From the dev machine, several hosts at once

Needs key-based SSH — `ssh-copy-id root@pve0` first if it asks.

```bash
cd ~/Projects/Homelab/setup/devpc
./servers/deploy.sh --dry-run root@pve0
./servers/deploy.sh root@pve0 root@node0 root@node1 root@node2
```

With the extra CLI tools (`jq`, `tree`, `htop`):

```bash
./servers/deploy.sh --with-tools root@pve0 root@node0 root@node1 root@node2
```

### On a single host, no clone

```bash
curl -fsSL https://raw.githubusercontent.com/feyzekrn/Homelab/main/setup/devpc/servers/bootstrap.sh | bash
```

Pinned to a tag instead of `main` — the safer form for anything you run as root:

```bash
curl -fsSL https://raw.githubusercontent.com/feyzekrn/Homelab/v1.0/setup/devpc/servers/bootstrap.sh | bash -s -- --ref v1.0
```

Then `exec bash`, or log in again.

---

## E. Changing The Look

**Switch the colour scheme** — eleven are available, listed in [terminal-designs.md](./terminal-designs.md#the-palettes):

```bash
cd ~/Projects/Homelab/setup/devpc/starship
sed -i '' 's/^PALETTE = .*/PALETTE = "dracula"/' gen.py
python3 gen.py
cp starship.toml ~/.config/starship.toml
```

**Change the spacing:**

```bash
cd ~/Projects/Homelab/setup/devpc/starship
sed -i '' 's/^SPACE_IN_BLOCK = .*/SPACE_IN_BLOCK = 0/' gen.py   # no blank line before the ❯
sed -i '' 's/^SPACE_ABOVE = .*/SPACE_ABOVE = 2/' gen.py         # more air between blocks
python3 gen.py && cp starship.toml ~/.config/starship.toml
```

**Push the change to every host afterwards** — commit and push first, the hosts fetch from GitHub:

```bash
cd ~/Projects/Homelab
git add setup/devpc/starship/starship.toml && git commit -m "prompt: switch palette" && git push
setup/devpc/servers/deploy.sh root@pve0 root@node0 root@node1 root@node2
```

> ⚠️ Never edit `starship.toml` directly. The generator overwrites it, and Nerd Font icons do not survive ordinary editing — [the reason](./terminal-designs.md#why-the-config-is-generated).

---

## F. Checking It Works

```bash
starship --version                     # is it installed
starship timings                       # per-module time, and any config warnings
starship explain                       # what each part of the current prompt means
python3 gen.py                         # prints the worst contrast in the palette
```

`starship timings` is the one to reach for when something looks off — it prints a warning line for any format string it could not parse.

---

## G. Undoing It

**Restore the previous config** (the script backs up before every overwrite):

```bash
ls ~/.dotfiles-backup/                       # pick a timestamp
cp ~/.dotfiles-backup/<timestamp>/.zshrc ~/.zshrc
cp ~/.dotfiles-backup/<timestamp>/starship.toml ~/.config/starship.toml
exec zsh
```

**Remove the tooling entirely:**

```bash
brew uninstall starship zsh-autosuggestions zsh-syntax-highlighting jq
rm ~/.config/starship.toml
```

**On a host:**

```bash
rm /usr/local/bin/starship ~/.config/starship.toml
sed -i '/starship init bash/d;/# Starship prompt/d' ~/.bashrc
```

---

## Troubleshooting

| Symptom | Cause | Fix |
|---|---|---|
| Icons show as empty boxes | Nerd Font missing or not selected | `brew install --cask font-jetbrains-mono-nerd-font`, then pick it in Warp |
| Icons look cramped | The **Mono** font variant is selected | Switch to `JetBrainsMono Nerd Font` without *Mono* |
| Prompt is plain on a server | starship not initialised for that shell | `echo 'eval "$(starship init bash)"' >> ~/.bashrc` |
| A coloured stub with nothing in it | Editing `starship.toml` by hand broke a separator | Re-run `python3 gen.py` |
| Icons vanished after an edit | Private Use Area glyphs got stripped | Re-run `python3 gen.py` — never edit the TOML |
| `starship: command not found` on a host | `/usr/local/bin` not on root's PATH | Log in again, or `export PATH=/usr/local/bin:$PATH` |
| Warp keeps resetting the font | Warp was running while the script edited its settings | Close Warp, re-run, or set it in the UI |
