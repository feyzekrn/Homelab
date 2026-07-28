# TrueNAS SCALE 🗄️ NAS

[← Back to Storage](../README.md)

TrueNAS SCALE is a full NAS operating system: Debian-based, ZFS at its core, administered entirely through a web interface, with built-in sharing (SMB, NFS, iSCSI), snapshot and replication management, user handling, alerting and an app catalogue. In a homelab it is normally run as a virtual machine with the storage controller passed through to it.

It is documented here as the **main alternative** to the chosen [ZFS-on-host approach](../zfs-nas) — and it is the option most homelabs pick, so the reasoning against it deserves to be explicit.

---

## Why It Is Documented

- It is the reference NAS platform: what most guides, forum threads and YouTube builds assume.
- The UI makes ZFS approachable — pool creation, dataset properties, snapshot schedules, replication jobs and scrub reports are all guided instead of memorised.
- Sharing is a first-class feature with proper user and permission management, rather than a hand-written Samba config.
- Built-in alerting: disk errors, pool degradation and failed scrubs surface on their own, which is exactly the kind of thing a hand-rolled setup forgets.

---

## Why It Is Not Chosen

**It takes ownership of the disks.** Passing the storage through to a VM means every consumer must go through the network — including the Immich, Jellyfin and Nextcloud containers running on the very same host. That removes the bind-mount architecture this project is built around, where an exposed app in a DMZ still reads its dataset at local disk speed without a single packet crossing the firewall.

Three more costs follow from that:

- **RAM.** TrueNAS wants 8–16 GB to be comfortable — on a 32 GB host, that is a large share taken from VMs and containers before anything useful runs.
- **A second system to maintain.** Its own updates, its own users, its own release cycle, on a host that already runs ZFS natively.
- **A boot dependency.** The family's photos become unreachable not when the host fails, but when *either* the host or the NAS VM fails.

None of this makes TrueNAS a bad product. It is the right answer when the NAS is a dedicated machine — which is exactly the scenario worth revisiting if this homelab ever gets separate storage hardware.

---

## Comparison Notes

| System | Best at | Trade-off |
|---|---|---|
| [ZFS on host + share container](../zfs-nas) | Local bind-mounts, minimal overhead, one system to maintain (chosen here) | No NAS UI — snapshots and pools are managed by hand |
| TrueNAS SCALE | Guided ZFS management, real sharing UI, alerting | Owns the disks, needs 8–16 GB RAM, adds a second OS |
| [OpenMediaVault](../openmediavault) | Lighter NAS UI on plain Debian | Weaker ZFS story, smaller feature set |
| Unraid | Mixed-size disks, easy expansion | Commercial licence, not ZFS-based |

---

## Runtime Status

`⚫ Inactive` and not planned. The [ZFS-on-host approach](../zfs-nas) is chosen; this page exists for comparison and as the natural candidate should storage ever move to dedicated hardware.

---

## Documentation

- [TrueNAS SCALE documentation](https://www.truenas.com/docs/scale/)
- [Wikipedia: TrueNAS](https://en.wikipedia.org/wiki/TrueNAS)
