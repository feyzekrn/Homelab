# Talos Linux — Getting Started

[← Back to Talos Linux](./README.md)

This guide gets written when phase 2 actually starts — Talos moves quickly, and a walkthrough written a year in advance would be stale on day one. The rough shape is already clear:

1. **Generate the image** via the [image factory](https://factory.talos.dev/) (schematic with the needed system extensions), record version and checksum in the [README](./README.md).
2. **Write the image to USB** — same macOS `dd` workflow as in the [Ubuntu guide](../ubuntu-server-24.04/getting-started.md#1-create-the-bootable-usb-macos), with one extra step first:

   ```bash
   xz -dk ./talos-metal-amd64-<version>.raw.xz
   ```

3. **Boot each node from the stick** — Talos starts in maintenance mode, no interactive installer.
4. **Apply declarative machine configs** with `talosctl` (control planes first, then workers) and bootstrap the cluster — all configs live in Git before the first boot, not after.

Unlike the Ubuntu phase there is no SSH and no manual post-install routine: everything after the boot is `talosctl` and Kubernetes APIs.
