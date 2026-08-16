# Talos Linux

[← Back to OS Strategy](../README.md)

Talos Linux is planned for phase 2 of the homelab.

After roughly one year of running Ubuntu Server 26.04 LTS, all nodes are expected to be wiped and rebuilt with Talos. This is the real bare-metal Kubernetes phase: immutable nodes, declarative machine configuration and infrastructure as code from the beginning. The full reasoning lives in the [OS Strategy](../README.md).

**In this folder:** [Getting Started](./getting-started.md) — the install walkthrough; gets written when the rebuild starts.

---

## Image Metadata

| Field | Value |
|---|---|
| OS | Talos Linux |
| Platform | metal |
| Architecture | amd64 |
| Filename | `talos-metal-amd64-<version>.raw.xz` or generated schematic image |
| Source | <https://www.talos.dev/> |
| Image factory | <https://factory.talos.dev/> |
| Downloaded | TBD |
| SHA256 verified | TBD |

The exact Talos version should be chosen when the rebuild starts, not during the Ubuntu learning phase. Talos moves quickly, so this document intentionally does not pin a future version yet.

---

## Target Nodes

| Node | Install status | Notes |
|---|---|---|
| Node 1 | Future | Control-plane candidate |
| Node 2 | Future | Control-plane candidate |
| Node 3 | Future | Control-plane candidate |

---

## Local File Placement

Place the downloaded or generated Talos image here locally:

```text
setup/compute/k8s-cluster/os/talos/talos-metal-amd64-<version>.raw.xz
```

The image itself should not be committed to Git.
