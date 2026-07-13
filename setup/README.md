# Setup & Hardware

This section covers every hardware decision made for this cluster — what was bought, what was salvaged from old machines, what it costs to run and why each component was chosen. The goal is that anyone reading this can understand the full reasoning and replicate or adapt it for their own build.

---

## Plan Overview

The cluster consists of three identical mini PCs connected through a single managed switch. Each node runs a dual-cable setup: one port for management traffic, one for cluster data. The hardware was chosen to be affordable enough to start immediately, efficient enough to run 24/7 at home without noise or significant electricity cost, and upgradeable enough to grow without replacing the base platform.

Everything reusable was taken from old hardware first. Only what was actually missing got purchased new or used from eBay.

---

## Sections

### [🖥️ Compute — Nodes, CPU, RAM & Storage](./compute)

The three Lenovo ThinkCentre M910q Tiny nodes that form the cluster. What was bought, what came from old hardware, why this platform was chosen and what the upgrade path looks like for CPU, RAM and storage. The [operating system running on these nodes](./compute/os) lives in the same folder — hardware and its OS in one place.

### [🌐 Networking — Switches & Physical Topology](./networking)

The MikroTik CRS310 as the central 2.5G data switch and why Layer 3 routing on the switch level matters for Kubernetes. Also covers the planned 1G management extension and how the dual-cable setup works. The [network design](./networking/design.md) (VLANs, DHCP, firewall zones) and the [MikroTik configuration](./networking/mikrotik) with its Terraform live in the same folder — the purchase decision and the living config side by side.

### [🔋 Power Supply — PSU, DC/DC Converter & Fuse Box](./power-supply)

How the cluster is powered cleanly and safely. Covers the power supply unit, DC/DC conversion for the nodes, fuse box setup and the reasoning behind centralising power distribution instead of running individual adapters per device.

---

## 💰 Total Cost Breakdown

✅ = purchased · ⬜ = still needed

| Status | Item                               | Qty |  Unit price |       Total |
| :----: | ---------------------------------- | --: | ----------: | ----------: |
|   ✅   | M910q Tiny barebone                |   3 |      ~ 32 € |      ~ 96 € |
|   ✅   | Intel i5-6500T CPU                 |   3 |      ~ 16 € |      ~ 48 € |
|   ✅   | Samsung 850 Pro SSD 256 GB         |   2 |      ~ 30 € |      ~ 60 € |
|   ✅   | Samsung 850 Pro SSD 256 GB         |   1 | from old PC |         0 € |
|   ✅   | 16 GB DDR4 SODIMM (Node 1)         |   1 | from old PC |         0 € |
|   ✅   | 8 GB DDR4 SODIMM (Node 2)          |   1 | from old PC |         0 € |
|   ✅   | 8 GB DDR4 SODIMM (Node 3)          |   1 |      ~ 15 € |      ~ 15 € |
|   ✅   | ARCTIC MX-4 (4g) Thermal Paste     |   1 |       ~ 5 € |       ~ 5 € |
|   ✅   | 2.5G M.2 network adapter           |   3 |      ~ 18 € |      ~ 54 € |
|        |                                    |     |             |             |
|   ⬜   | MikroTik CRS310                    |   1 |     ~ 180 € |     ~ 180 € |
|   ⬜   | Patch Panel 12-Port Cat.6a 10" 1HE |   1 |      ~ 35 € |      ~ 35 € |
|   ⬜   | 0.25m Slim Patch Cables            |  10 |       ~ 2 € |      ~ 20 € |
|   ⬜   | PSU MEAN WELL MW UHP-500-24        |   1 |      ~ 75 € |      ~ 75 € |
|   ⬜   | DC-DC Step-Down Converter 20A      |   1 |      ~ 25 € |      ~ 25 € |
|   ⬜   | KFZ Fuse Box 6-Port                |   1 |       ~ 8 € |       ~ 8 € |
|   ⬜   | Kill Switch + fuses + cable        |   1 |      ~ 20 € |      ~ 20 € |
|        |                                    |     |             |             |
|        |                                    |     |             |             |
|        | **Total (all listed parts)**       |     |             | **~ 641 €** |
|        | **Already spent** ✅               |     |             | **~ 278 €** |
|        | **Still outstanding** ⬜           |     |             |  **~ 363€** |

---

## 🔌 Running Costs (24/7, €0.35/kWh)

| Device           | Scenario  |        Watt |       Per month |    Per year |
| ---------------- | --------- | ----------: | --------------: | ----------: |
| 1× Node          | Idle      |     ~ 5–8 W |   ~ 1.28–2.04 € |   ~ 15–25 € |
| 1× Node          | Default   |   ~ 10–15 W |   ~ 2.56–3.83 € |   ~ 31–46 € |
| 1× Node          | Full load |   ~ 35–40 W |  ~ 8.94–10.22 € |  ~ 107–123 € |
|                  |           |             |                 |             |
| MikroTik CRS310  | Idle      |      ~ 21 W |        ~ 5.37 € |      ~ 64 € |
| MikroTik CRS310  | Default   |      ~ 27 W |        ~ 6.90 € |      ~ 83 € |
| MikroTik CRS310  | Full load |      ~ 34 W |        ~ 8.69 € |     ~ 104 € |
|                  |           |             |                 |             |
|                  |           |             |                 |             |
| 3 nodes + switch | Idle      |   ~ 36–45 W |  ~ 9.20–11.50 € | ~ 110–138 € |
| 3 nodes + switch | Default   |   ~ 57–72 W | ~ 14.56–18.40 € | ~ 175–221 € |
| 3 nodes + switch | Full load | ~ 139–154 W | ~ 35.51–39.35 € | ~ 426–472 € |
|                  |           |             |                 |             |
| 5 nodes + switch | Idle      |   ~ 46–61 W | ~ 11.75–15.59 € | ~ 141–187 € |
| 5 nodes + switch | Default   |  ~ 77–102 W | ~ 19.67–26.06 € | ~ 236–313 € |
| 5 nodes + switch | Full load | ~ 209–234 W | ~ 53.40–59.79 € | ~ 641–717 € |
|                  |           |             |                 |             |
| 7 nodes + switch | Idle      |   ~ 56–77 W | ~ 14.31–19.67 € | ~ 172–236 € |
| 7 nodes + switch | Default   |  ~ 97–132 W | ~ 24.78–33.73 € | ~ 297–405 € |
| 7 nodes + switch | Full load | ~ 279–314 W | ~ 71.28–80.23 € | ~ 855–963 € |
