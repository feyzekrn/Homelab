# Ubuntu Server 26.04 LTS

[← Back to OS Strategy](../README.md)

Ubuntu Server 26.04 LTS is used for phase 1 of the homelab.

It is installed on all Lenovo M910q Tiny nodes for the first learning-focused cluster build. This phase is about building strong Linux, Kubernetes, cloud-native and networking fundamentals before the later Talos rebuild. The full reasoning lives in the [OS Strategy](../README.md).

**In this folder:** [Getting Started](./getting-started.md) — step by step from bootable USB to a freshly updated node with SSH access.

---

## Image Metadata

| Field | Value |
|---|---|
| OS | Ubuntu Server |
| Release line | 26.04 LTS (Resolute Raccoon, released 2026-04-20) |
| Architecture | amd64 |
| Filename | `ubuntu-26.04-live-server-amd64.iso` |
| Size | 2,918,598,656 bytes (2.72 GiB) |
| Source | <https://ubuntu.com/download/server> |
| Checksum source | <https://releases.ubuntu.com/26.04/SHA256SUMS> |
| Official SHA256 | `dec49008a71f6098d0bcfc822021f4d042d5f2db279e4d75bdd981304f1ca5d9` |
| Downloaded | 2026-08-13 |
| SHA256 verified | ✅ **Match** (2026-08-13) — local copy hashes identically, size matches to the byte |

Large ISO files stay out of Git — the ISO can be placed in this folder locally; the repository tracks version, source URL and checksum only.

---

## Why 26.04 Instead of 24.04

The OS strategy was written while 24.04 was the current LTS. By the time the first node was actually prepared, **26.04 LTS had shipped (2026-04-20)** and 24.04 was a release behind.

Nothing in the phase-1 reasoning depends on the point release. The argument is "a full general-purpose Linux server that exposes its internals rather than hiding them" — 26.04 satisfies that exactly as well, with a newer kernel, a support window running to 2031 instead of 2029, and current container tooling.

Two things worth keeping in mind for the Kubernetes phase:

- Kubernetes packages come from the upstream `pkgs.k8s.io` repositories, not from Ubuntu's own archive — so the Ubuntu release line barely influences which Kubernetes version can be installed.
- Installer screens shift slightly between releases. The [getting-started guide](./getting-started.md) describes 26.04; on a different release, read the screens rather than assuming they match.

---

## Target Nodes

| Node | Install status | Notes |
|---|---|---|
| Node 1 | Planned | First control-plane candidate |
| Node 2 | Planned | Worker or additional control-plane candidate |
| Node 3 | Planned | Worker or additional control-plane candidate |

---

## Local File Placement

The downloaded ISO lives here locally:

```text
setup/compute/k8s-cluster/os/ubuntu-server-26.04/ubuntu-26.04-live-server-amd64.iso
```

The ISO itself is not committed to Git — `*.iso` is covered by the repository's `.gitignore`.
