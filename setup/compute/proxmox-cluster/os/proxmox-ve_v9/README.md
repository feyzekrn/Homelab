# Proxmox VE

[← Back to Operating System](../README.md)

Proxmox VE is the hypervisor OS for the MS-01 (`pve0`). This page tracks the exact installer version.

**In this folder:** [Getting Started](./getting-started.md) — step by step from bootable USB (macOS, no Rufus) through the installer to the first update.

---

## Image Metadata

| Field | Value |
|---|---|
| OS | Proxmox VE |
| Version | 9.2 (web UI reports 9.2.2 after first update) |
| Architecture | amd64 |
| Filename | `proxmox-ve_9.2-1.iso` |
| Source | <https://www.proxmox.com/en/downloads> |
| Checksum source | <https://enterprise.proxmox.com/iso/SHA256SUMS> |
| Official SHA256 | `4e88fe416df9b527624a175f24c9aa07c714d3332afb1ee3dbf3879573ef2c6c` |
| Downloaded | 2026-07 |
| SHA256 verified | ❌ **Mismatch** (2026-07-29): local copy hashes to `26c52c70…` at the correct size — a few corrupted blocks in the download. Re-download before the next install; `pve0` itself installed and updated fine. |

Large ISO files stay out of Git — the ISO can be placed in this folder locally; the repository tracks version, source URL and checksum only.

---

## Target Machines

| Machine | Install status | Notes |
|---|---|---|
| `pve0` (MS-01) | ✅ Installed | Graphical installer, ext4 on the 1 TB NVMe, static management IP |
