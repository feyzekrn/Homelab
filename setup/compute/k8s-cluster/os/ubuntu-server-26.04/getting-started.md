# Ubuntu Server 26.04 — Getting Started

[← Back to Ubuntu Server 26.04 LTS](./README.md)

Step by step from a downloaded ISO to a freshly updated node that can be reached over SSH. Written for the Lenovo M910q Tiny nodes, prepared from a Mac.

---

## 1. Create the Bootable USB (macOS)

macOS ships everything needed: `diskutil` to manage the stick and `dd` to write the image. The Ubuntu Server ISO is a hybrid image and can be written raw to a USB stick as-is — no Rufus, no Etcher required.

**Verify the checksum first:**

```bash
shasum -a 256 ~/Downloads/ubuntu-26.04-live-server-amd64.iso
```

Compare against the value in [Image Metadata](./README.md#image-metadata) / <https://releases.ubuntu.com/26.04/SHA256SUMS>. Doing this *before* writing saves debugging an installer that fails halfway through.

**Identify the USB stick:**

```bash
diskutil list external
```

Find the stick by its size and name (e.g. `/dev/disk4`, listed as *external, physical*). **Double-check this — writing to the wrong disk destroys its data.** `external` in the filter is deliberate: it keeps the internal NVMe out of the output entirely.

**Clear the stick (unmount, not eject):**

```bash
diskutil unmountDisk /dev/diskX
```

If the stick still carries a previous installer image, macOS re-mounts its partitions the moment they appear and `dd` fails with `Resource busy`. Wiping the partition table is the reliable fix — nothing left to mount, nothing that can re-mount:

```bash
diskutil eraseDisk free EMPTY /dev/diskX
```

**Write the ISO:**

```bash
sudo dd if=/Users/<user>/Downloads/ubuntu-26.04-live-server-amd64.iso of=/dev/rdiskX bs=1m
```

Details that matter:

- `rdiskX` (with the `r`) instead of `diskX` — the raw device is several times faster. `~2.9 GB` takes roughly 100 seconds at ~30 MB/s
- `bs=1m` — without a block size, `dd` writes in 512-byte chunks and the write takes hours. `bs=4m` works too
- **No `status=progress`** — that is GNU `dd` syntax and macOS does not accept it. Press **Ctrl+T** during the write to print the current progress instead
- **`~` is already `/Users/<user>`.** A path like `~/Users/<user>/Downloads/...` expands to `/Users/<user>/Users/<user>/Downloads/...` and fails with `No such file or directory`. Easiest way to avoid it: type `sudo dd if=` and then drag the ISO from Finder into the Terminal window
- macOS may show a "disk not readable" popup afterwards — expected (the stick now carries a Linux filesystem). Click *Ignore*, **not** *Initialize*

A successful run ends with a byte count that matches the ISO size exactly:

```text
2783+1 records in
2783+1 records out
2918598656 bytes transferred in 97.559106 secs (29916210 bytes/sec)
```

**Flush and eject:**

```bash
sync
diskutil eject /dev/diskX
```

### If `dd` fails

| Message | Cause | Fix |
|---|---|---|
| `No such file or directory` | Path wrong — usually a doubled `~/Users/<user>/` | Drag the ISO into Terminal, or use exactly one of `~/Downloads/…` or `/Users/<user>/Downloads/…` |
| `Resource busy` | A partition of the stick is mounted | `diskutil unmountDisk /dev/diskX`, or `diskutil eraseDisk free EMPTY /dev/diskX` if it keeps re-mounting |
| `Operation not permitted` | Terminal lacks disk access | System Settings → Privacy & Security → Full Disk Access → enable Terminal, then restart Terminal |
| Nothing happens for minutes | Normal — `dd` is silent | Ctrl+T for progress |

---

## 2. Boot the Node from the Stick

1. Plug in the stick, power on the M910q and press **F12** for the boot menu (**F1** enters BIOS setup if boot options need changing).
2. Pick the USB stick as boot device.
3. Choose **Try or Install Ubuntu Server** in the GRUB menu.

If the stick does not appear in the boot menu at all, disable Secure Boot in BIOS setup and retry.

---

## 3. Walk Through the Installer

The installer (Subiquity) runs in a text UI — arrow keys, `Tab` and `Enter` to navigate. The choices that matter:

1. **Language / keyboard** — as preferred.
2. **Installation type** — *Ubuntu Server* (the default, not *minimized*: this phase is for learning, the standard tooling should be there).
3. **Network** — the installer picks up DHCP on the wired interface. Note the address it gets; a stable address per node (static or reservation) is handled as part of the network setup, not here.
4. **Proxy / mirror** — leave empty / defaults.
5. **Storage** — *Use an entire disk* on the internal disk. LVM (default) is fine. Confirming this step **erases the disk**.
6. **Profile** — hostname per node (e.g. `node1`), a personal admin user and a strong password. No root password is set — the admin user uses `sudo`.
7. **SSH Setup** — ✅ **check "Install OpenSSH server"**. This is the important one: it makes the node reachable remotely right after the first boot. Optionally import SSH keys from GitHub here (`Import SSH identity: from GitHub` + username) — then key-based login works immediately.
8. **Featured server snaps** — select **none**. Kubernetes components are installed deliberately later, not as snaps.

When the install finishes, choose **Reboot Now** and remove the stick when prompted.

---

## 4. First Login and Update

Log in on the console (or directly via SSH, see below) with the user from step 6, then bring the system fully up to date:

```bash
sudo apt update && sudo apt full-upgrade -y
```

If a kernel update was installed, reboot once:

```bash
sudo reboot
```

Two useful checks after the reboot:

```bash
ip -brief addr        # which interface has which IP
systemctl status ssh  # OpenSSH server running?
```

---

## 5. SSH from the Mac

With the OpenSSH server installed, connect from the Mac:

```bash
ssh <user>@<node-ip>
```

On first connect, accept the host-key fingerprint with `yes`.

**Key-based login** (skip if keys were already imported from GitHub in the installer):

```bash
ssh-keygen -t ed25519    # only if no key exists yet on the Mac
ssh-copy-id <user>@<node-ip>
```

After `ssh-copy-id`, login works without a password prompt.

**Convenience — an entry in `~/.ssh/config` on the Mac:**

```text
Host node1
    HostName <node-ip>
    User <user>
```

Then `ssh node1` is enough.

---

## 6. Done — What Comes Next

The node is installed, updated and reachable over SSH. From here the cluster work starts — each part documented as it gets built:

- repeat for the remaining nodes
- basic hardening (SSH key-only login, firewall) — as part of the Ansible-based provisioning
- container runtime and Kubernetes installation
