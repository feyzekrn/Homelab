# Proxmox VE — Getting Started

[← Back to Proxmox VE](./README.md)

Step by step from a downloaded ISO to a clean, current Proxmox VE node — as done on `pve0`. Covers the **macOS bootable-USB workflow** (no Rufus needed — Rufus is Windows-only anyway; on macOS the built-in tools do the job), the installer choices and the mandatory post-install routine. The post-install part takes about 15 minutes and happens entirely in the web UI — no SSH needed.

---

## 1. Create the Bootable USB on macOS (no Rufus)

macOS ships everything needed: `diskutil` to manage the stick and `dd` to write the image. The Proxmox ISO is a hybrid image — it can be written raw to a USB stick as-is.

**Identify the USB stick:**

```bash
diskutil list
```

Find the stick by its size and name (e.g. `/dev/disk4`, listed as *external, physical*). **Double-check this — writing to the wrong disk destroys its data.**

**Unmount it (unmount, not eject):**

```bash
diskutil unmountDisk /dev/diskX
```

**Write the ISO:**

```bash
sudo dd if=./proxmox-ve_9.2-1.iso of=/dev/rdiskX bs=4m status=progress
```

Details that matter:

- `rdiskX` (with the `r`) instead of `diskX` — the raw device is several times faster
- `bs=4m` — larger block size, also for speed
- macOS may show a "disk not readable" popup afterwards — that is expected (the stick now carries a Linux filesystem). Click *Ignore*, **not** *Initialize*.

**Flush and eject:**

```bash
sync
diskutil eject /dev/diskX
```

---

## 2. Run the Installer

Boot the target machine from the stick and choose *Install Proxmox VE (Graphical)* — the terminal UI options are only fallbacks for display problems or serial-console setups.

The choices as made on `pve0`:

- **Target disk:** the internal NVMe (`/dev/nvme0n1`), default ext4 + LVM layout
- **FQDN:** `pve0.internal` — the part before the first dot becomes the node name and is effectively permanent; the domain part is easy to change later
- **Management IP:** static, deliberately placed **outside the router's DHCP pool** (high host number) — no conflict possible by construction, and the address does not depend on the router remembering anything. `pve0` runs on `192.168.178.250/24`; why it stays static rather than becoming a DHCP reservation is argued in the [router docs](../../../../networking/router/README.md#addressing-after-the-swap)
- **Management interface:** the installer asks which NIC carries it, and writes exactly **one** into the bridge. On a four-port machine like the MS-01 the other three stay unconfigured — a cable in the wrong socket gives a link light and nothing else. See [the note below](#if-the-web-ui-is-unreachable-after-a-network-change)
- **No network needed during install:** the installer writes the static config regardless; the machine can be installed offline and cabled later

**After the reboot:** remove the stick when prompted. The web UI is at `https://<management-ip>:8006` (self-signed certificate — the browser warning is expected), login `root` + the password set during installation. The console login prompt on the physical screen can be ignored; all services run without it.

---

## 3. First Login

Open `https://<management-ip>:8006` in a browser:

- The **certificate warning** is expected (self-signed certificate) → *Advanced* → *Proceed*.
- Login: user `root`, the password set during installation, realm **Linux PAM standard authentication**. PAM means "check against the Linux users of the system" — `root` is exactly that. The *Proxmox VE authentication server* realm is a separate, UI-only user database that starts empty.
- The popup **"No valid subscription"** appears on every login. It is not an error — it just notes that the free repository is used. Click *OK*.

To silence it permanently, patch the check out of the web UI's JavaScript (node → *Shell*), then hard-reload the browser:

```bash
sed -i.bak "s/data.status.toLowerCase() !== 'active'/false/g" /usr/share/javascript/proxmox-widget-toolkit/proxmoxlib.js && systemctl restart pveproxy
```

Two caveats: this edits a packaged file, so **every update of `proxmox-widget-toolkit` brings the popup back** and the command has to run again — `grep -c` for the same pattern first if a future version has renamed it. And `.bak` next to it is the original, in case the substitution ever hits more than intended.

> If the realm dropdown is ever **empty**, the page loaded without its API call completing (flaky connection). Hard-reload with `Cmd+Shift+R`.

---

## 4. Switch the Package Repositories

A fresh installation points at the **enterprise repository**, which requires a paid subscription — every update fails until this is changed.

**Node → Updates → Repositories:**

1. Select the row with `https://enterprise.proxmox.com/debian/pve` → **Disable**
2. Click **Add** → choose **No-Subscription** → confirm

<img src="../../../../schematics/proxmox-first-steps-repositories.png" alt="Proxmox repository configuration: enterprise repo disabled, no-subscription repo added" width="900">

The result should look like above: the `pve-no-subscription` repository enabled, the `pve-enterprise` repository disabled (`Enabled: false`). The Debian rows stay untouched; the Ceph no-subscription repository can stay or be disabled — it is unused without Ceph, and its warning is informational only.

---

## 5. Install the First Updates

**Node → Updates:**

1. **Refresh** — reads the package lists (`apt-get update`). The task should end with `TASK OK` and show packages coming from `download.proxmox.com/debian/pve ... pve-no-subscription`.
2. **Upgrade** — opens a live terminal running `apt full-upgrade`. Click into the window, answer `Do you want to continue? [Y/n]` with `y` + Enter and let it run.
3. When the prompt returns (`root@pve0:~#`), the upgrade is done — type `exit` (or close the window).

<img src="../../../../schematics/proxmox-first-steps-updates.png" alt="Proxmox updates view: Refresh first, then Upgrade" width="900">

4. **Reboot** (top right) — the first update almost always ships a new kernel, which needs one boot to become active. The node is back in ~2 minutes.

---

## 6. Changing the Management IP Later

Needed when the router is replaced and the subnet changes with it — a static address does not follow its gateway. Done once already, when the [Speedport gave way to the Fritz!Box](../../../../networking/router/README.md#addressing-after-the-swap) and the house moved from `192.168.2.0/24` to `192.168.178.0/24`.

Three files, all on the node:

| File | What changes |
|---|---|
| `/etc/network/interfaces` | `address` and `gateway` in the `vmbr0` block — not in the `enp…` block above it, which stays `inet manual` |
| `/etc/hosts` | the line carrying the node name; **the one people forget.** Proxmox resolves its own name through it, and a stale entry breaks the web UI and any later cluster join |
| `/etc/resolv.conf` | `nameserver` |

Then `reboot` (or *System → Network → Apply Configuration*). Verify with `ip -4 addr show vmbr0` and a ping to the new gateway.

The same edits exist in the GUI — *System → Network* for the bridge, *System → DNS* for the resolver, the built-in *Shell* for `/etc/hosts`. The catch is that the GUI has to be reachable, and after a subnet change it is not. Either do it at the physical console, or give a laptop a second address in the **old** subnet first (`sudo ifconfig en0 alias 192.168.2.100 255.255.255.0` on macOS — a router bridges its LAN and WLAN into one segment, so no cable is needed).

### If the web UI is unreachable after a network change

The console shows the right address, the network shows nothing. Almost always the **cable is in the wrong socket**.

The IP does not belong to the machine, it belongs to `vmbr0` — a Linux bridge, i.e. a software switch — and exactly one physical NIC is plugged into that bridge via `bridge-ports`. Traffic only flows through that one. Unlike a router, where all sockets are internally bridged into one network, every NIC in a PC is an independent device with its own MAC, and Proxmox configures only the one chosen at install time.

```bash
ip -br link
```

The NIC showing `UP` and `LOWER_UP` must be the one named in `bridge-ports`. To find out which socket is which physically, blink its LED:

```bash
ethtool -p enp2s0f0 10
```

The permanent fix, if the guessing is annoying: bond both NICs, then either socket works and a pulled cable does not take the node offline.

---

## 7. Done — What Comes Next

The base system is now clean and current. Follow-ups, each documented as it gets built:

- Storage layout (ZFS pool for guest data)
- VLAN-aware bridge on the trunk port
- First guests: see the [target layout](../../README.md#what-will-run-here)
- Dedicated users: a personal admin user with 2FA, and a `terraform@pve` API token once IaC touches this machine — day-to-day work should not run as `root`
