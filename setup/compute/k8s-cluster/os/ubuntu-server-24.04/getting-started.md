# Ubuntu Server 24.04 — Getting Started

[← Back to Ubuntu Server 24.04 LTS](./README.md)

Step by step from a downloaded ISO to a freshly updated node that can be reached over SSH. Written for the Lenovo M910q Tiny nodes, prepared from a Mac.

---

## 1. Create the Bootable USB (macOS)

Download the ISO (see [Image Metadata](./README.md#image-metadata)) and verify its checksum:

```bash
shasum -a 256 ./ubuntu-24.04.x-live-server-amd64.iso
```

Compare against the value from <https://releases.ubuntu.com/24.04/> and record it in the README.

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
sudo dd if=./ubuntu-24.04.x-live-server-amd64.iso of=/dev/rdiskX bs=4m status=progress
```

- `rdiskX` (with the `r`) instead of `diskX` — the raw device is several times faster
- macOS may show a "disk not readable" popup afterwards — expected (the stick now carries a Linux filesystem). Click *Ignore*, **not** *Initialize*.

**Flush and eject:**

```bash
sync
diskutil eject /dev/diskX
```

---

## 2. Boot the Node from the Stick

1. Plug in the stick, power on the M910q and press **F12** for the boot menu (**F1** enters BIOS setup if boot options need changing).
2. Pick the USB stick as boot device.
3. Choose **Try or Install Ubuntu Server** in the GRUB menu.

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
