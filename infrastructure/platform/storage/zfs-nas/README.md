# ZFS Pool + Share Container 🗄️ NAS

[← Back to Storage](../README.md)

This is the **chosen NAS approach**: the ZFS pool lives directly on the Proxmox host, and a small container exports what needs to be reachable over the network. There is no NAS operating system in the middle.

It is a deliberate inversion of the usual homelab reflex ("install TrueNAS in a VM"), and the reason is the access pattern — most consumers of this storage do not want a network share at all.

---

## The Layout

One pool, one dataset per purpose:

```text
tank                     # ZFS pool on the Proxmox host
├── tank/media           # Jellyfin library
├── tank/immich          # Photo originals
├── tank/nextcloud       # Personal cloud data
├── tank/k8s-cold        # Cold storage for cluster apps (NFS export)
└── tank/backups         # Velero/Longhorn backup target (via MinIO)
```

Each dataset carries its own quota, its own snapshot schedule and its own sharing rules. Immich cannot fill the backup dataset, media needs no hourly snapshots, and the cluster export is restricted to the node IPs.

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

## Operational Notes

- **A mirror is not a backup.** ZFS survives a dead disk, not a deleted library, ransomware or a lightning strike. The irreplaceable datasets (`immich`, `nextcloud`) need a copy off the box — `zfs send` to an external disk or an encrypted cloud target.
- **Start with 2 disks as a mirror**, extend later with a second mirror pair in the same pool (striped mirrors). More space and more throughput without a rebuild.
- **ZFS wants RAM.** The ARC cache will happily take several gigabytes; plan for it when sizing VMs on the same host.
- **Scrub monthly**, and make sure the result actually reaches a notification channel.

---

## Runtime Status

`⚫ Inactive` — the pool is planned as the first real workload on [`pve0`](../../../../setup/compute/proxmox-cluster) once additional disks are installed. The MS-01 currently holds a single NVMe drive carrying the hypervisor itself.

---

## Documentation

- [OpenZFS documentation](https://openzfs.github.io/openzfs-docs/)
- [Proxmox VE ZFS documentation](https://pve.proxmox.com/wiki/ZFS_on_Linux)
- [Wikipedia: ZFS](https://en.wikipedia.org/wiki/ZFS)
