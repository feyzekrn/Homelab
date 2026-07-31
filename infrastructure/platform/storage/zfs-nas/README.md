# ZFS Pool + Share Container 🗄️ NAS

[← Back to Storage](../README.md)

This is the **chosen NAS approach**: the ZFS pool lives directly on the Proxmox host, and a small container exports what needs to be reachable over the network. There is no NAS operating system in the middle.

It is a deliberate inversion of the usual homelab reflex ("install TrueNAS in a VM"), and the reason is the access pattern — most consumers of this storage do not want a network share at all.

---

## The Hardware: Two Tiers

| Tier | Disk | Holds |
|---|---|---|
| **Fast** | 1× 1 TB NVMe *(already installed)* | Proxmox itself, VM and LXC root disks, anything latency-sensitive |
| **Bulk** | 2× 2 TB HDD as a ZFS mirror → **2 TB usable** | The `tank` pool: media, photos, personal cloud, backups |

The split is deliberate. Media streaming and photo storage are sequential workloads that gain almost nothing from NVMe, so the money goes into capacity rather than speed. The NVMe keeps carrying the things where latency actually shows — the hypervisor, the container root filesystems, the databases.

**2 TB usable is a real constraint** and should be planned against rather than discovered. It is comfortable for a photo library and a personal cloud, tight for a large media collection, and it shares space with the cluster backup target. Quotas per dataset are what keep one consumer from eating the others.

---

## The Layout

One pool, one dataset per purpose:

```text
tank                     # ZFS mirror, 2 TB usable
├── tank/media           # Jellyfin library — read-only to the app
├── tank/immich          # Photo originals — irreplaceable
├── tank/nextcloud       # Personal cloud data — irreplaceable
├── tank/k8s-cold        # Cold storage for cluster apps (NFS export)
└── tank/backups         # Velero/Longhorn backup target (via MinIO)
```

Each dataset carries its own quota, its own snapshot schedule and its own sharing rules. Immich cannot fill the backup dataset, media needs no hourly snapshots, and the cluster export is restricted to the node IPs.

**Growth path:** a mirror is extended by adding a second mirror pair to the same pool (striped mirrors), which adds capacity and throughput without a rebuild or a migration. Two more 2 TB disks later means 4 TB usable. Starting with a mirror rather than a single disk is what keeps that door open.

---

## How Each Consumer Reaches It

| Consumer | Path | Why |
|---|---|---|
| Immich, Jellyfin, Nextcloud (LXCs on the same host) | **Bind-mount** from the host | Local filesystem access — no network packet involved, full disk speed, and the app's network zone becomes irrelevant to its storage |
| Kubernetes apps needing cold storage | **NFS export** of `tank/k8s-cold`, consumed through the NFS CSI driver | Big and slow data does not belong on Longhorn replicas |
| Velero / Longhorn backups | **[MinIO](../minio)** with `tank/backups` as its data directory | S3 is what the backup tools speak |
| Family devices | **SMB share** through the share container | What phones and laptops expect |

The bind-mount row is the important one. It is why an exposed app like Jellyfin can sit caged in a DMZ VLAN and still read the media library at local speed: the storage path does not cross the network, so the firewall zone costs it nothing. Where an app must write (Immich), it gets exactly one dataset, and read-only wherever possible (Jellyfin).

---

## Why Not A NAS Operating System

The moment the disks are handed to a [TrueNAS](../truenas) VM, they belong to that VM. Every consumer — including the containers sitting a few centimetres away on the same host — has to go through NFS or SMB. That trades away local-speed bind-mounts, adds a network hop to every photo thumbnail, and makes the storage layer depend on a second operating system booting correctly.

What is given up in exchange is real: a polished web UI, guided snapshot and replication management, dashboards, alerting and a supported upgrade path. That is the honest trade — **operational convenience against architectural simplicity** — and this project takes the second, because the host is already a ZFS-capable system that has to be maintained anyway.

---

## What Runs In The Container

A minimal LXC with:

- **Samba** for family shares
- **NFS server** for the cluster export
- optionally **Cockpit** with the file-sharing module, if a browser UI becomes desirable

The pool itself is not managed there — `zfs` commands and the Proxmox UI handle datasets, snapshots and scrubs on the host. The container only publishes.

**Networking:** two interfaces — one in the services VLAN for family access through the firewall, one directly in the cluster VLAN so NFS and S3 traffic reaches the nodes unrouted. One NAS, two faces.

---

## Prerequisites

| Requirement | Why |
|---|---|
| **2× 2 TB HDD installed in `pve0`** | The pool cannot exist without them — this is the hard blocker |
| Proxmox VE running | ZFS is managed by the host, not by a guest OS |
| RAM headroom | The ARC cache takes several gigabytes; size the VMs around it |
| A VLAN plan | The share container needs a leg in the services VLAN and one in the cluster VLAN |

**What this blocks:** [Jellyfin](../../../../applications/jellyfin), [Immich](../../../../applications/immich), [Nextcloud](../../../../applications/nextcloud), [MinIO (backup)](../minio) and therefore [Velero](../../backup/velero). It is the single highest-leverage purchase left in the build — roughly 110 € that unblocks four components and the entire backup story.

---

## Operational Notes

- **A mirror is not a backup.** ZFS survives a dead disk, not a deleted library, ransomware or a lightning strike. The irreplaceable datasets (`immich`, `nextcloud`) need a copy off the box — `zfs send` to an external disk or an encrypted cloud target.
- **ZFS wants RAM.** The ARC cache will happily take several gigabytes; plan for it when sizing VMs on the same host. With 32 GB total and a [`pve-node` VM](../../../../setup/compute/README.md#the-bridge-one-node-with-a-foot-in-both-worlds) now permanently in the cluster, this is worth budgeting rather than assuming.
- **Scrub monthly**, and make sure the result actually reaches a notification channel.
- **Set quotas before filling datasets.** Retrofitting a quota onto a full dataset is a migration; setting it on an empty one is one command.

---

## Runtime Status

`⚫ Inactive` — the pool is the **first real workload** planned on [`pve0`](../../../../setup/compute/proxmox-cluster), waiting only on the two HDDs. The MS-01 currently holds a single NVMe drive carrying the hypervisor itself.

Nothing else in the Proxmox world is blocked by this: [AdGuard Home](../../dns/adguard-home), [Vaultwarden](../../security/password-manager/bitwarden), [Caddy](../../ingress/caddy) and [NetBird](../../ingress/netbird) all run from the NVMe and deliver value today. The pool is what unlocks the data-heavy half.

---

## Documentation

- [OpenZFS documentation](https://openzfs.github.io/openzfs-docs/)
- [Proxmox VE ZFS documentation](https://pve.proxmox.com/wiki/ZFS_on_Linux)
- [Wikipedia: ZFS](https://en.wikipedia.org/wiki/ZFS)
