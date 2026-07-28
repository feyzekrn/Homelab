# OpenMediaVault 🗄️ NAS

[← Back to Storage](../README.md)

OpenMediaVault (OMV) is a NAS distribution built on plain Debian, administered through a web interface. It covers the classic NAS job — disks, filesystems, SMB/NFS shares, users, S.M.A.R.T. monitoring, scheduled jobs — with a much smaller footprint than [TrueNAS](../truenas), and it runs happily on modest hardware including a Raspberry Pi.

It is documented as a **secondary alternative** to the chosen [ZFS-on-host approach](../zfs-nas).

---

## Why It Is Documented

- It is the lightweight answer when a NAS UI is wanted but 8–16 GB of RAM for TrueNAS is not available.
- Debian underneath means everything learned about Linux administration still applies — no appliance lock-in.
- Its plugin system covers the common needs (rsync, Docker via the compose plugin, S.M.A.R.T. reporting) without turning into an app store.
- For readers of this repository building a *standalone* NAS box on old hardware, it is often the most sensible starting point.

---

## Why It Is Not Chosen

The same structural objection as TrueNAS applies: **a NAS OS wants to own the disks**, which breaks the bind-mount architecture where family apps read their datasets locally on the same host.

On top of that, OMV's ZFS support is a plugin rather than a core feature. This project's storage design leans heavily on ZFS datasets, snapshots and `zfs send` — putting that on a plugin layer of a distribution that is fundamentally happier with ext4/btrfs would mean accepting a NAS UI *and* a weaker ZFS story. If a NAS operating system were chosen at all, TrueNAS would be the better fit.

---

## Comparison Notes

| System | Best at | Trade-off |
|---|---|---|
| [ZFS on host + share container](../zfs-nas) | Local bind-mounts, one system, full ZFS (chosen here) | No NAS UI |
| [TrueNAS SCALE](../truenas) | The strongest ZFS-plus-UI combination | 8–16 GB RAM, owns the disks |
| OpenMediaVault | Light NAS UI on ordinary Debian, runs on weak hardware | ZFS only via plugin, fewer features |

---

## Runtime Status

`⚫ Inactive` and not planned.

---

## Documentation

- [OpenMediaVault documentation](https://docs.openmediavault.org/)
- [Wikipedia: OpenMediaVault](https://en.wikipedia.org/wiki/OpenMediaVault)
