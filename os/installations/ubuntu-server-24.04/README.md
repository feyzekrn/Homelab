# Ubuntu Server 24.04 LTS Installer

[← Back to Installation Media](../README.md)

Ubuntu Server 24.04 LTS is used for phase 1 of the homelab.

It is installed on all Lenovo M910q Tiny nodes for the first learning-focused cluster build. This phase is about building strong Linux, Kubernetes, cloud-native and networking fundamentals before the later Talos rebuild.

---

## Image Metadata

| Field | Value |
|---|---|
| OS | Ubuntu Server |
| Release line | 24.04 LTS |
| Architecture | amd64 |
| Filename | `ubuntu-24.04.x-live-server-amd64.iso` |
| Source | <https://ubuntu.com/download/server> |
| Checksum source | <https://releases.ubuntu.com/24.04/> |
| Downloaded | TBD |
| SHA256 verified | TBD |

Use the latest available 24.04 LTS point-release ISO when preparing the USB stick, then update the filename and checksum fields above.

---

## Target Nodes

| Node | Install status | Notes |
|---|---|---|
| Node 1 | Planned | First control-plane candidate |
| Node 2 | Planned | Worker or additional control-plane candidate |
| Node 3 | Planned | Worker or additional control-plane candidate |

---

## Local File Placement

Place the downloaded ISO here locally:

```text
os/installations/ubuntu-server-24.04/ubuntu-24.04.x-live-server-amd64.iso
```

The ISO itself should not be committed to Git.

---

## USB Write Example

From the repository root:

```bash
sudo dd if=./os/installations/ubuntu-server-24.04/ubuntu-24.04.x-live-server-amd64.iso of=/dev/rdiskX bs=4m status=progress
sync
```

Replace `diskX` with the actual USB disk from `diskutil list`.
