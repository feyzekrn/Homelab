# OS Installation Media

[← Back to OS Strategy](../README.md)

This directory is the staging area for bootable operating system installers used by the homelab.

The goal is to keep the exact installer versions documented while avoiding large binary files in Git. Downloaded ISO and image files can be placed here locally and written directly to a USB stick when needed.

---

## Directory Layout

```text
setup/compute/os/installations/
├── ubuntu-server-24.04/
│   └── README.md
└── talos/
    └── README.md
```

---

## USB Writing Workflow

On macOS, identify the USB stick first:

```bash
diskutil list
```

Unmount the USB stick before writing:

```bash
diskutil unmountDisk /dev/diskX
```

Write the image:

```bash
sudo dd if=./IMAGE_FILE.iso of=/dev/rdiskX bs=4m status=progress
```

Flush writes and eject:

```bash
sync
diskutil eject /dev/diskX
```

Replace `diskX` with the actual USB disk. Using the wrong disk destroys data.

---

## Tracked Metadata

For every installer image, document:

- OS name
- exact version
- filename
- source URL
- checksum source
- verified checksum
- date downloaded
- target nodes

This makes it clear which image was installed, even after the actual ISO or raw image is removed locally.
