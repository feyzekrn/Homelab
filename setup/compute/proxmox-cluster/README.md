# 🐙 proxmox-cluster — The Infrastructure Workstation

[← Back to Compute Overview](../README.md)

**In this folder:** [`./os`](./os) — Proxmox VE as the hypervisor OS, including the macOS bootable-USB workflow.

---

## The Platform: Minisforum MS-01 Workstation × 1

The stable half of the homelab. While the Tiny nodes form the experimentation field, this machine is the **infrastructure anchor**: it will carry the NAS, the router/firewall (OPNsense), DNS, the family-facing apps — and it can spin up VMs as additional Kubernetes nodes when the cluster needs support.

Bought as a **complete bundle** — RAM and SSD were already installed, which made the price hard to beat compared to buying the barebone and parts separately.

> ⚠️ **This machine is optional.** The homelab works without it — the Kubernetes cluster on three mini PCs is the core of this project, and it costs less than a third of what this workstation did. See [the compute overview](../README.md#-the-proxmox-host-is-optional) for what the MS-01 provides and how each of those things can be solved differently. It was added when the lab started holding data other people depend on, not at the beginning.

| Part                                    | Qty | Details                                                          |    What I paid | Where to find it                                                                     |
| --------------------------------------- | --: | ---------------------------------------------------------------- | -------------: | ------------------------------------------------------------------------------------ |
| Minisforum MS-01 Workstation             |   1 | Intel Core i9-12900H (14C/20T), 2× 10G SFP+, 2× 2.5G RJ45, PCIe x16 slot | ~ 500 € (bundle) | [eBay](https://www.ebay.de/sch/i.html?_nkw=Minisforum+MS-01) · [Minisforum](https://store.minisforum.de/) |
| Corsair Vengeance 32 GB DDR5-4800 SODIMM |   1 | CMSX64GX5M2A4800C40 kit stick — came installed in the bundle      |       included | [Amazon](https://www.amazon.de/s?k=corsair+vengeance+ddr5+sodimm+4800)               |
| fanxiang S880 1 TB NVMe SSD              |   1 | M.2 2280, PCIe 4.0 — came installed in the bundle                 |       included | [Amazon](https://www.amazon.de/s?k=fanxiang+s880+1tb)                                |
| WiFi module *(model TBD)*                |   1 | Salvaged from an old PC — see below                               |            0 € | —                                                                                    |

> **Bundle tip:** The MS-01 is regularly listed used with RAM and SSD already installed. A bundle around ~500 € beats buying barebone + parts separately — just verify what exactly is included and that the seller states the CPU variant correctly (i5-12600H, i9-12900H and i9-13900H versions exist).

---

### Why the Minisforum MS-01?

The MS-01 is built for exactly this role — a small workstation with server-grade connectivity:

- **Networking is the headline feature:** 2× **10G SFP+** and 2× **2.5G RJ45** onboard. The SFP+ ports are the future trunk into the MikroTik CRS310 — all VLANs tagged over one fast link, with room for the storage traffic of the whole homelab. No other mini PC in this price class brings native 10G.
- **Enough compute to host a second world:** the i9-12900H (14 cores / 20 threads, 45 W base) comfortably runs OPNsense, a NAS, a handful of LXCs *and* still has headroom for one or two VMs that join the Kubernetes cluster as extra worker nodes when needed.
- **A real PCIe 4.0 x16 slot** (x8 electrical, low-profile): the designated path for a future GPU — turning this box into the central AI machine (LLM inference, Immich ML, transcoding) without touching the rest of the setup.
- **Three M.2 NVMe slots** (one U.2-capable): storage can grow from the single 1 TB stick to a proper tiered layout — fast NVMe pool for VMs, dedicated disks for the NAS datasets.
- **Intel vPro/AMT** (depending on CPU SKU — to be verified in the BIOS/MEBx): out-of-band management for the cross-watchdog concept, where the k8s side can power-cycle this machine even when the OS is dead.

The role split against the Tiny nodes is deliberate: this machine is a **pet, not cattle**. It is allowed to be unique, it holds state (family data, router config) and it is not part of any experiment. Everything that must survive tinkering lives here; everything that benefits from replication lives on the cluster.

### What it was actually bought for

Honesty about the purchase, because the feature list above makes it sound more necessary than it is:

- **It was not bought to be a router.** OPNsense occupies 2 vCPU and a few gigabytes here. A 25 € Fritz!Box plus the switch would carry the household's routing without complaint — that part is pure convenience.
- **It was bought because the cluster cannot hold data.** Three nodes with 256 GB SATA SSDs leave roughly 250 GB usable after replication, the Tiny chassis has no room for a 3.5" HDD, and 8–16 GB of RAM per node disappears quickly once Immich's machine learning and a few databases join the cluster components. A photo and media library simply does not fit.
- **A used office desktop for ~100 € would have met that requirement.** The surcharge for this machine buys 10G networking, a silent 20 W idle box instead of a bulky one, modern transcoding, and a PCIe slot for a future GPU.

The full comparison — including why a Raspberry Pi NAS is the expensive-looking-cheap option — is in the [compute overview](../README.md#the-honest-cheap-alternatives).

> ⚠️ **GPU compatibility:** The PCIe slot takes **low-profile, max. dual-slot** cards only — and the MS-01 PSU is external (DC-in), so power-hungry GPUs are out. Plan for cards in the RTX A2000 / RTX 4000 SFF class.

---

### The WiFi Module — Salvaged

The MS-01 bundle came without a WiFi card, but it has a free M.2 2230 (A+E key) slot for one. Instead of buying, the module was **pulled from an old PC** that was not in use anymore — same approach as the salvaged parts on the Tiny nodes: check what old hardware still contains before spending money.

| Part                      | Qty | Where it came from        | Approx. value |
| ------------------------- | --: | ------------------------- | ------------: |
| WiFi module *(model TBD)* |   1 | Salvaged from an old PC   |    ~ 10–20 € |

To be clear about its role: **the hypervisor itself never runs over WiFi** (bridged VM traffic and WLAN do not mix — the module is there for flexibility, e.g. passing it through to a VM later).

---

## Naming

The Kubernetes nodes are cattle — numbered, replaceable (`node0`–`node2`). This machine is the opposite, but its name stays deliberately functional: **`pve0`** (FQDN `pve0.internal`), following the same generic scheme so every machine in the homelab is instantly recognizable by role. If a second Proxmox node ever joins, it becomes `pve1`.

The `.internal` domain is used instead of made-up TLDs like `.lan` or `.home`: it is officially reserved by ICANN for private networks (like `home.arpa`, but shorter) — guaranteed to never collide with public DNS.

---

## What Will Run Here

The target layout for this machine — each guest documented in its own section as it gets built:

| Guest                  | Type      | Role                                                    |
| ---------------------- | --------- | ------------------------------------------------------- |
| OPNsense               | VM        | Router, firewall, inter-VLAN gateway                     |
| NAS                    | VM / LXC  | ZFS datasets, NFS/SMB shares, MinIO S3 for cluster backups |
| Nextcloud, Jellyfin, Immich | LXC  | Family-facing apps with bind-mounted datasets            |
| Caddy                  | LXC       | Reverse proxy for the Proxmox world                      |
| AdGuard Home (primary) | LXC       | DNS + filtering, synced to a replica on the cluster      |
| Responder              | LXC       | Watchdog for the k8s nodes (health checks + vPro revive) |
| Reserve k8s workers    | VM        | Join the cluster on demand when extra capacity is needed |
| AI workloads *(later)* | VM + GPU  | Central AI box once a GPU is installed                   |

---

## Upgrade Path

**Short term**

- Second RAM stick: the bundle stick is one half of a 2× 32 GB kit — adding the matching stick doubles RAM to **64 GB** without replacing anything

**Mid term**

- Populate the free M.2 slots: dedicated NVMe for VM storage, keeping the OS disk clean
- SATA/USB or U.2 storage for the NAS datasets once it takes over file duties

**Long term**

- RAM up to **96 GB** (2× 48 GB DDR5 SODIMM) — the official maximum
- **Low-profile GPU** in the PCIe slot → the central AI machine
- A second MS-01 (`pve1`) if the Proxmox world ever needs real failover
