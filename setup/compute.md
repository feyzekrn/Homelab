# 🖥️ Compute — Nodes, CPU, RAM & Storage

[← Back to Setup Overview](./README.md)

---

## The Platform: Lenovo ThinkCentre M910q Tiny × 3

The foundation of the cluster. Three identical mini PCs, bought as **barebones on eBay** — meaning they came with a weak Pentium CPU and no RAM. That is completely fine because both get replaced anyway.

| Part                                     | Details                                                        |    What I paid | Where to find it                                                                                |
|------------------------------------------|----------------------------------------------------------------|---------------:|-------------------------------------------------------------------------------------------------|
| Lenovo ThinkCentre M910q Tiny (barebone) | Pentium, no RAM — both get replaced                            |    ~ 32 € each | [eBay listing](https://www.ebay.de/itm/136979171958?_skw=Lenovo+ThinkCentre+M910q+Tiny+pentium) |
| Intel Core i5-6500T (CPU)                | Quad-core, 35 W TDP, fits the M910q                            |    ~ 16 € each | [eBay](https://www.ebay.de/sch/i.html?_nkw=Intel+i5-6500T)                                      |
| 8 GB DDR4 SODIMM                         | Gerenal compunting power                                       |    ~ 18 € each | [eBay](https://www.ebay.de/sch/i.html?_nkw=ddr4+8gb+sodimm&_sacat=0&_from=R40&_trksid=p2332490.m570.l1313)                                         |
| 256 GB Samsung 850 Pro SATA SSD          | For OS, container images and Longhorn storage                  | ~ 29.90 € each | [Amazon](https://www.amazon.de/s?k=Samsung+870+256GB+SSD)                                       |
| 2.5G M.2 Ethernet Adapter                | Extra NIC via the M.2 slot                                     |    ~ 18 € each | [Amazon](https://www.amazon.de/s?k=2.5g+m.2+ethernet+adapter)                                   |
| ARCTIC MX-4 (4g) Thermalpaste            | Needed for replacing the CPU ( you can get something cheaper ) |     ~ 5 € each | [Amazon](https://www.amazon.de/ARCTIC-MX-4-Gramm-Hochleistungs-W%C3%A4rmeleitpaste-W%C3%A4rmeleitf%C3%A4higkeit-niedrigem-thermischen-Widerstand/dp/B07L9BDY3T/ref=asc_df_B07L9BDY3T?mcid=25a894fac819387b9f1f191652defc8b&th=1&psc=1&tag=googshopde-21&linkCode=df0&hvadid=697141436093&hvpos=&hvnetw=g&hvrand=946606344809581304&hvpone=&hvptwo=&hvqmt=&hvdev=c&hvdvcmdl=&hvlocint=&hvlocphy=9042486&hvtargid=pla-600861085163&psc=1&hvocijid=946606344809581304-B07L9BDY3T-&hvexpln=0)                                   |

> **eBay tip:** Listings with a Pentium or Celeron and no RAM are usually the cheapest — and that is perfectly fine since you replace both anyway. Just check the condition of the chassis and power supply.

---

### Why the Lenovo ThinkCentre M910q Tiny?

The M910q Tiny hits a very specific sweet spot for a homelab cluster. The machine supports **Intel vPro**, which means the hardware is designed for managed business environments — better stability and longer driver support than typical consumer hardware.

It takes **6th and 7th generation Intel CPUs** (Skylake / Kaby Lake), which means you can start cheap with an i5-6500T and later upgrade to an **i7-7700T** when you actually need the extra headroom. The i7-7700T is still a T-chip, so it stays within the same 35 W TDP — you get a meaningful CPU upgrade without any increase in power consumption or thermal load.

The form factor is also a deliberate choice. These machines are silent, compact and realistic for 24/7 operation at home. Electricity cost and noise matter much more over a full year than raw peak performance.

> ⚠️ **CPU compatibility:**
>
> - The M910q Tiny supports **Intel 6th gen (Skylake) and 7th gen (Kaby Lake) only**. Newer or older generations are not compatible, regardless of socket appearance.

---

### Why the M.2 2.5G Network Adapter?

The M910q Tiny has an M.2 slot that sits unused in the default configuration. Adding a 2.5G adapter there gives each node a second physical network interface. The plan is to use **both ports separately**: the onboard 1G port for management traffic — SSH, monitoring, fallback — and the 2.5G M.2 adapter for actual cluster traffic. Kubernetes inter-node communication, Longhorn replication, databases and message brokers all go over the fast 2.5G path. This way the two traffic types never compete for bandwidth on the same cable.

---

## Parts From Old Hardware — What You Can Reuse

Before buying everything new it is worth checking what you already have at home. Old laptops and desktop PCs often contain usable components. I pulled parts from two different machines.

| Part                            | Where it came from |  Approx. value |
|---------------------------------|---|---------------:|
| 16 GB DDR4 SODIMM               | Had a spare stick from another PC |  ~ 25 € – 35 € |
| 8 GB DDR4 SODIMM                | Pulled from a second unused PC |   ~ 15 € –20 € |
| 256 GB Samsung 850 Pro SATA SSD | Already had one |  ~ 25 € – 30 € |

If you have old laptops or desktop PCs sitting unused, check whether they contain DDR4 SODIMM RAM or a SATA SSD before spending money on new parts.

> ⚠️ **RAM compatibility — check these three things before pulling anything:**
>
> - It must be **SODIMM** form factor. Full-size DIMMs from desktop PCs will not fit.
> - It must be **DDR4**. The M910q Tiny only works with DDR4. DDR3 SODIMMs will not fit physically and DDR3L will not work either.

---

## Upgrade Path

**Short term**
- Upgrade Node 2 & 3 RAM to 16 GB when workloads actually demand it

**Mid term**
- Add a fourth and fifth node — the MikroTik still has 5 free 2.5G ports

**Long term**
- Upgrade CPUs to **Intel Core i7-7700T** for a meaningful performance jump without touching power draw. The i5-6500T runs 4 cores and 4 threads. The i7-7700T adds **Hyper-Threading**, giving 8 threads instead — which noticeably helps with parallel Kubernetes workloads. Both are T-chips with the same 35 W TDP.
- Upgrade RAM up to **64 GB per node** (2× 32 GB DDR4 SODIMM). The M910q Tiny only has **2 RAM slots**, so the maximum is reached with two sticks. Keep this in mind from the start: if you run a single 16 GB stick now, leave the second slot free — that way you can add a second stick later without throwing anything away. Going to 64 GB means replacing both sticks entirely.
- Swap SSDs for larger ones if storage becomes the bottleneck