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

### [🌐 Networking — Switches & Physical Topology](./networking.md)
The MikroTik CRS310 as the central 2.5G data switch and why Layer 3 routing on the switch level matters for Kubernetes. Also covers the planned 1G management extension and how the dual-cable setup works.

### [🔋 Power Supply — PSU, DC/DC Converter & Fuse Box](./power-supply.md)
How the cluster is powered cleanly and safely. Covers the power supply unit, DC/DC conversion for the nodes, fuse box setup and the reasoning behind centralising power distribution instead of running individual adapters per device.

---

## 💰 Total Cost Breakdown

| Item | Qty | Unit price | Total |
|---|---:|---:|---:|
| M910q Tiny barebone | 3 | ~ 32 € | ~ 96 € |
| Intel i5-6500T CPU | 3 | ~ 16 € | ~ 48 € |
| Samsung 870 SSD 256 GB | 2 | ~ 29.90 € | ~ 59.80 € |
| Samsung 870 SSD 256 GB | 1 | from old PC | 0 € |
| 2.5G M.2 network adapter | 3 | ~ 18 € | ~ 54 € |
| MikroTik CRS310 | 1 | ~ 180 € | ~ 180 € |
| 16 GB DDR4 SODIMM (Node 1) | 1 | from old PC | 0 € |
| 8 GB DDR4 SODIMM (Node 2) | 1 | from old PC | 0 € |
| 8 GB DDR4 SODIMM (Node 3) | 1 | ~ 15 € | ~ 15 € |
| | | | |
| Total | | | ~ 452.80 € |

---

## 🔌 Running Costs (24/7, €0.35/kWh)
 
| Device | Scenario | Watt | Per month | Per year |
|---|---|---:|---:|---:|
| 1× Node | Idle | ~ 10–15 W | ~ 2.56–3.83 € | ~ 31–46 € |
| 1× Node | Default | ~ 20–25 W | ~ 5.11–6.39 € | ~ 61–77 € |
| 1× Node | Full load | ~ 35 W | ~ 8.94 € | ~ 107 € |
| | | | | |
| MikroTik CRS310 | Idle | ~ 21 W | ~ 5.37 € | ~ 64 € |
| MikroTik CRS310 | Default | ~ 27 W | ~ 6.90 € | ~ 83 € |
| MikroTik CRS310 | Full load | ~ 34 W | ~ 8.69 € | ~ 104 € |
| | | | | |
| | | | | |
| 1 node + switch | Idle | ~ 31–36 W | ~ 7.92–9.20 € | ~ 95–110 € |
| 1 node + switch | Default | ~ 47–52 W | ~ 12.01–13.29 € | ~ 144–160 € |
| 1 node + switch | Full load | ~ 69 W | ~ 17.63 € | ~ 212 € |
| | | | | |
| 3 nodes + switch | Idle | ~ 51–66 W | ~ 13.03–16.87 € | ~ 156–202 € |
| 3 nodes + switch | Default | ~ 87–102 W | ~ 22.23–26.06 € | ~ 267–313 € |
| 3 nodes + switch | Full load | ~ 139 W | ~ 35.53 € | ~ 426 € |
| | | | | |
| 5 nodes + switch | Idle | ~ 71–96 W | ~ 18.14–24.53 € | ~ 218–295 € |
| 5 nodes + switch | Default | ~ 127–152 W | ~ 32.45–38.84 € | ~ 389–467 € |
| 5 nodes + switch | Full load | ~ 209 W | ~ 53.40 € | ~ 641 € |
| | | | | |
| 7 nodes + switch | Idle | ~ 91–126 W | ~ 23.25–32.20 € | ~ 279–386 € |
| 7 nodes + switch | Default | ~ 167–202 W | ~ 42.67–51.61 € | ~ 512–620 € |
| 7 nodes + switch | Full load | ~ 279 W | ~ 71.29 € | ~ 856 € |