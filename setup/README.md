# Setup & Hardware

This section covers every hardware decision made for this cluster — what was bought, what was salvaged from old machines, what it costs to run and why each component was chosen. The goal is that anyone reading this can understand the full reasoning and replicate or adapt it for their own build.

---

## Plan Overview

The cluster consists of three identical mini PCs connected through a single managed switch. Each node runs a dual-cable setup: one port for management traffic, one for cluster data. The hardware was chosen to be affordable enough to start immediately, efficient enough to run 24/7 at home without noise or significant electricity cost, and upgradeable enough to grow without replacing the base platform.

Everything reusable was taken from old hardware first. Only what was actually missing got purchased new or used from eBay.

---

## Sections

### [🖥️ Compute — Nodes, CPU, RAM & Storage](./compute.md)
The three Lenovo ThinkCentre M910q Tiny nodes that form the cluster. What was bought, what came from old hardware, why this platform was chosen and what the upgrade path looks like for CPU, RAM and storage.

### [🔌 Networking — Switches & Physical Topology](./networking.md)
The MikroTik CRS310 as the central 2.5G data switch and why Layer 3 routing on the switch level matters for Kubernetes. Also covers the planned 1G management extension and how the dual-cable setup works.

---

## 💰 Total Cost Breakdown

| Item | Qty |  Unit price |            Total |
|---|----:|------------:|-----------------:|
| M910q Tiny barebone |   3 |      ~ 32 € |       **~ 96 €** |
| Intel i5-6500T CPU |   3 |      ~ 16 € |       **~ 48 €** |
| Samsung 870 SSD 256 GB |   2 |   ~ 29.90 € |    **~ 59.80 €** |
| Samsung 870 SSD 256 GB |   1 | from old PC |          **0 €** |
| 2.5G M.2 network adapter |   3 |      ~ 18 € |       **~ 54 €** |
| MikroTik CRS310 |   1 |     ~ 180 € |      **~ 180 €** |
| 16 GB DDR4 SODIMM (Node 1) |   1 | from old PC |          **0 €** |
| 8 GB DDR4 SODIMM (Node 2) |   1 | from old PC |          **0 €** |
| 8 GB DDR4 SODIMM (Node 3) |   1 |      ~ 15 € |       **~ 15 €** |
| **Total** |     |             |   **~ 452.80 €** |

---

## 🔌 Running Costs (24/7, €0.35/kWh)

| Device | Idle usage |                Per month |            Per year |
|---|---:|-------------------------:|--------------------:|
| 1× Node | ~ 6–10 W |        ~ 1.55 € – 2.56 € |       ~ 18 € – 31 € |
| MikroTik CRS310 | ~ 21–34 W |        ~ 5.40 € – 8.70 € |      ~ 64 € – 104 € |
| | |                          |                     |
| **Total — 3 nodes + switch** | **~ 39–64 W** |  **~ 10.05 € – 16.38 €** | **~ 120 € – 197 €** |
| **Total — 5 nodes + switch** | **~ 51–84 W** |  **~ 13.13 € – 21.50 €** | **~ 157 € – 258 €** |
| **Total — 7 nodes + switch** | **~ 63–104 W** |  **~ 16.13 € – 26.62 €** | **~ 194 € – 319 €** |

---