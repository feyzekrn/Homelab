# 🖧 Servers — The Same Prompt On The Machines

[← Back to Dev PC](../README.md)

This folder is not about a dev machine. It exists because of one property of shell prompts that surprises people:

**A prompt is generated on the machine the shell runs on.** SSH into `pve0` and the prompt you see was produced by a shell process on `pve0`. Your Mac's Starship is not involved. So if you want the Proxmox host to identify itself, Starship has to be installed there.

The good news is how little that costs.

---

## What Goes On A Host

| | |
|---|---|
| `/usr/local/bin/starship` | One static binary, ~9 MB, no dependencies |
| `~/.config/starship.toml` | The same file the Mac uses, fetched directly from GitHub |
| One line in `~/.bashrc` | `eval "$(starship init bash)"` |

That is the complete footprint. Three things, all removable with `rm` and one `sed`.

## What Deliberately Does Not

**No zsh.** Starship works with bash, and bash is what root uses on Proxmox and on the Ubuntu nodes. Installing a second shell to get a nicer prompt would be the wrong trade on a machine whose job is to run VMs.

**No fonts.** The host sends Unicode code points down the SSH connection; your terminal renders them with the font on your machine. A Debian install with no fonts at all still shows the Proxmox icon correctly.

**No clone.** The scripts fetch individual files over HTTPS. There is no repository on the host, so there is nothing to leave behind, nothing to go stale, and no git to install.

**No general provisioning.** This is the shell environment and, optionally, three CLI tools. Package baselines, users, SSH hardening and the rest belong in [provisioning](../../../infrastructure/provisioning).

---

## The Two Scripts

### bootstrap.sh — run on the host

```bash
curl -fsSL https://raw.githubusercontent.com/feyzekrn/Homelab/main/setup/devpc/servers/bootstrap.sh | bash
```

```bash
./bootstrap.sh --dry-run       # print what would happen
./bootstrap.sh --with-tools    # also install jq, tree, htop
./bootstrap.sh --ref v1.0      # take the config from a tag rather than main
```

It detects the architecture (`x86_64`, `aarch64`, `armv7l`), downloads the matching Starship release, **verifies its SHA256** against the checksum published beside it, installs it, fetches the config and wires up `~/.bashrc`. It refuses to run on macOS and points at the other script.

Root is only needed to write into `/usr/local/bin`; it uses `sudo` for that single step if it is not already root.

### deploy.sh — run on the dev machine

```bash
./deploy.sh root@pve0
./deploy.sh --with-tools root@pve0 root@node0 root@node1 root@node2
./deploy.sh --dry-run root@pve0
```

This does **not** reimplement the installation. It pipes `bootstrap.sh` into the remote shell:

```bash
ssh "$host" bash -s -- "${REMOTE_ARGS[@]}" < bootstrap.sh
```

One installation path, one place to fix a bug. It checks connectivity first and reports per host at the end, so one unreachable node does not silently swallow the rest.

Requires key-based SSH (`ssh-copy-id root@pve0`) and outbound HTTPS from the host — the Starship release and the config both come from GitHub.

---

## What The Prompt Shows Per Machine

Detection is by filesystem, never by hostname, so a renamed or cloned machine still identifies itself correctly:

| Machine | Detected via | Icon |
|---|---|---|
| `pve0` — Proxmox VE | `/etc/pve` | `` |
| `node0`–`node2` — Kubernetes | `/var/lib/kubelet`, or k3s / RKE2 paths | `󱃾` |
| A container | `/.dockerenv`, `/run/.containerenv` | `` |
| Everything else | `/etc/os-release` | The distribution logo |

Containers are worth a note: they are short-lived and you do not want Starship baked into every image. If a container prompt matters, a single line in the image does the job — the font still comes from your terminal:

```bash
PS1='\[\e[1;34m\]\[\e[0m\] \h \w \$ '
```

---

## On Piping A Script Into A Shell

`curl … | bash` is a pattern worth being deliberate about, even for your own repository. Both scripts default to the `main` branch, which means a push changes what runs on your servers the next time you invoke it.

For anything you run as root, pin it:

```bash
curl -fsSL https://raw.githubusercontent.com/feyzekrn/Homelab/v1.0/setup/devpc/servers/bootstrap.sh | bash -s -- --ref v1.0
```

`--ref` controls where the *config* is fetched from; the URL controls which version of the *script* runs. Pin both to the same tag and the result is reproducible.

The Starship binary itself is verified by checksum regardless of which path you take.
