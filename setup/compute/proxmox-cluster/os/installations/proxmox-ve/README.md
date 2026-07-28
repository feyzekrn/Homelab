# Proxmox VE Installer

[← Back to OS — Proxmox VE](../../README.md)

Proxmox VE is the hypervisor OS for the MS-01 (`pve0`). This page tracks the exact installer version and documents the **macOS bootable-USB workflow** — no Rufus needed (Rufus is Windows-only anyway; on macOS the built-in tools do the job).

---

## Image Metadata

| Field | Value |
|---|---|
| OS | Proxmox VE |
| Version | TBD *(check with `pveversion` on the host)* |
| Architecture | amd64 |
| Filename | `proxmox-ve_x.y-z.iso` |
| Source | <https://www.proxmox.com/en/downloads> |
| Checksum source | shown next to the download link |
| Downloaded | 2026-07 |
| SHA256 verified | TBD |

---

## Target Machines

| Machine | Install status | Notes |
|---|---|---|
| `pve0` (MS-01) | ✅ Installed | Graphical installer, ext4 on the 1 TB NVMe, static management IP |

---

## Creating the Bootable USB on macOS (no Rufus)

macOS ships everything needed: `diskutil` to manage the stick and `dd` to write the image. The Proxmox ISO is a hybrid image — it can be written raw to a USB stick as-is.

**1. Identify the USB stick:**

```bash
diskutil list
```

Find the stick by its size and name (e.g. `/dev/disk4`, listed as *external, physical*). **Double-check this — writing to the wrong disk destroys its data.**

**2. Unmount it (unmount, not eject):**

```bash
diskutil unmountDisk /dev/diskX
```

**3. Write the ISO:**

```bash
sudo dd if=./proxmox-ve_x.y-z.iso of=/dev/rdiskX bs=4m status=progress
```

Details that matter:

- `rdiskX` (with the `r`) instead of `diskX` — the raw device is several times faster
- `bs=4m` — larger block size, also for speed
- macOS may show a "disk not readable" popup afterwards — that is expected (the stick now carries a Linux filesystem). Click *Ignore*, **not** *Initialize*.

**4. Flush and eject:**

```bash
sync
diskutil eject /dev/diskX
```

**5. Boot the target machine from the stick** and choose *Install Proxmox VE (Graphical)* — the terminal UI options are only fallbacks for display problems or serial-console setups.

---

## Installation Notes (as done on `pve0`)

- **Target disk:** the internal NVMe (`/dev/nvme0n1`), default ext4 + LVM layout
- **FQDN:** `pve0.internal` — the part before the first dot becomes the node name and is effectively permanent; the domain part is easy to change later
- **Management IP:** static, deliberately placed **outside the router's DHCP pool** (high host number) since the ISP router offers no address reservation — no conflict possible by construction
- **No network needed during install:** the installer writes the static config regardless; the machine can be installed offline and cabled later
- **After the reboot:** remove the stick when prompted. The web UI is at `https://<management-ip>:8006` (self-signed certificate — the browser warning is expected), login `root` + the password set during installation. The console login prompt on the physical screen can be ignored; all services run without it.
