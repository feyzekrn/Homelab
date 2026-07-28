# Proxmox VE — First Steps After Installation

[← Back to OS — Proxmox VE](./README.md)

The mandatory post-install routine on a fresh Proxmox VE node, as done on `pve0`. Takes about 15 minutes. Everything happens in the web UI — no SSH needed.

---

## 1. First Login

Open `https://<management-ip>:8006` in a browser:

- The **certificate warning** is expected (self-signed certificate) → *Advanced* → *Proceed*.
- Login: user `root`, the password set during installation, realm **Linux PAM standard authentication**. PAM means "check against the Linux users of the system" — `root` is exactly that. The *Proxmox VE authentication server* realm is a separate, UI-only user database that starts empty.
- The popup **"No valid subscription"** appears on every login. It is not an error — it just notes that the free repository is used. Click *OK*.

> If the realm dropdown is ever **empty**, the page loaded without its API call completing (flaky connection). Hard-reload with `Cmd+Shift+R`.

---

## 2. Switch the Package Repositories

A fresh installation points at the **enterprise repository**, which requires a paid subscription — every update fails until this is changed.

**Node → Updates → Repositories:**

1. Select the row with `https://enterprise.proxmox.com/debian/pve` → **Disable**
2. Click **Add** → choose **No-Subscription** → confirm

<img src="../../../schematics/proxmox-first-steps-repositories.png" alt="Proxmox repository configuration: enterprise repo disabled, no-subscription repo added" width="900">

The result should look like above: the `pve-no-subscription` repository enabled, the `pve-enterprise` repository disabled (`Enabled: false`). The Debian rows stay untouched; the Ceph no-subscription repository can stay or be disabled — it is unused without Ceph, and its warning is informational only.

---

## 3. Install the First Updates

**Node → Updates:**

1. **Refresh** — reads the package lists (`apt-get update`). The task should end with `TASK OK` and show packages coming from `download.proxmox.com/debian/pve ... pve-no-subscription`.
2. **Upgrade** — opens a live terminal running `apt full-upgrade`. Click into the window, answer `Do you want to continue? [Y/n]` with `y` + Enter and let it run.
3. When the prompt returns (`root@pve0:~#`), the upgrade is done — type `exit` (or close the window).

<img src="../../../schematics/proxmox-first-steps-updates.png" alt="Proxmox updates view: Refresh first, then Upgrade" width="900">

4. **Reboot** (top right) — the first update almost always ships a new kernel, which needs one boot to become active. The node is back in ~2 minutes.

---

## 4. Done — What Comes Next

The base system is now clean and current. Follow-ups, each documented as it gets built:

- Storage layout (ZFS pool for guest data)
- VLAN-aware bridge on the trunk port
- First guests: see the [target layout](../README.md#what-will-run-here)
- Dedicated users: a personal admin user with 2FA, and a `terraform@pve` API token once IaC touches this machine — day-to-day work should not run as `root`
