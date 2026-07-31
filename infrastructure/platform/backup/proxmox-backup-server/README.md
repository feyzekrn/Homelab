# Proxmox Backup Server

[← Back to Backup](../README.md)

Proxmox Backup Server (PBS) is the backup counterpart to Proxmox VE: a dedicated server that stores deduplicated, incremental, verifiable backups of virtual machines and containers. Where [Velero](../velero) covers the Kubernetes world, PBS covers the Proxmox world.

It is **planned for later** — the start is covered by the simpler mechanism already built into Proxmox VE.

---

## What It Does

- **Deduplicated, incremental backups.** Only changed chunks are transferred and stored. Ten daily snapshots of the same VM cost a fraction of ten full copies.
- **Verification.** Backups are checksummed and can be re-verified on a schedule, which turns "the backup exists" into "the backup is readable".
- **Live restore and single-file restore.** A VM can be booted directly from a backup while it restores in the background, and individual files can be pulled out of an image without restoring the whole guest.
- **Retention with pruning.** Keep-last / keep-daily / keep-weekly rules, applied automatically.
- **Remote sync.** One PBS instance can pull from another — the natural path to an off-site copy.

---

## Why Not Yet

Proxmox VE ships `vzdump`, which writes plain compressed backups of any guest to a directory on a schedule. Pointed at a dataset on the ZFS pool, that already provides the thing that matters most at this stage: **a restorable copy of every VM and container**, without a second server to install and maintain.

PBS becomes worth it when one of these becomes true:

- backup storage fills up, and deduplication would fix it
- restores need to be fast and selective rather than whole-guest
- the backups should live on separate hardware from the machines they protect

The last point is the important one, and it is also the reason PBS is not simply installed as a guest on `pve0` today: **a backup server on the machine it backs up protects against mistakes, not against losing the machine.** The sensible version is PBS on a separate box — an old PC, a Raspberry Pi with an external disk, or a small VPS — which is a hardware decision, not a software one.

---

## Planned Role

| Aspect | Plan |
|---|---|
| Runs on | A VM initially; separate hardware once available |
| Protects | The Proxmox guests: OPNsense, the share container, the family app containers |
| Does not protect | Kubernetes workloads — that is [Velero](../velero)'s job, targeting [MinIO](../../storage/minio) |
| Storage | Its own datastore, deliberately not the same pool it backs up |
| Off-site | Sync job to a second PBS instance or an encrypted cloud target |

The irreplaceable data (photos, personal cloud) is additionally covered at the dataset level by `zfs send`, as described in the [NAS documentation](../../storage/zfs-nas). Backups of the guests and backups of the data are two separate concerns, and neither substitutes for the other.

---

## Runtime Status

`⚫ Inactive` — planned once `vzdump` to the ZFS pool stops being sufficient, ideally together with dedicated backup hardware.

---

## Prerequisites

| Requirement | Why |
|---|---|
| Disks in `pve0` → [ZFS pool](../../storage/zfs-nas) | Even `vzdump` needs somewhere to write |
| A second machine or external disk | PBS on the host it backs up protects against mistakes, not against hardware loss |
| RAM headroom (~1–2 GB) | It brings its own OS as a VM |

**Start with `vzdump`, not with this.** Proxmox VE's built-in dump to the ZFS pool covers the family apps from day one and needs no extra component. PBS earns its place later, when deduplication and incremental backups matter — a full nightly dump of Immich's container is wasteful in a way a deduplicating store is not.

The genuinely important step is neither of them: **getting a copy off the machine.** `zfs send` to an external disk protects against the case both `vzdump` and PBS-on-the-same-host share — the box itself being gone.

---

## Documentation

- [Proxmox Backup Server documentation](https://pbs.proxmox.com/docs/)
- [Proxmox VE backup and restore](https://pve.proxmox.com/wiki/Backup_and_Restore)
