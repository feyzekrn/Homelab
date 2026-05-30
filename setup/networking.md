# 🔌 Networking — Switches & Physical Topology

[← Back to Setup Overview](./README.md)

---

## Core Switch: MikroTik CRS310-8G+2S+IN

The central switch for the whole cluster. Bought new, because this switch brings real features that actually matter for Kubernetes.

| Part | Details |        Price | Where to find it |
|---|---|-------------:|---|
| MikroTik CRS310-8G+2S+IN | 8× 2.5G ports + 2× SFP+ |      ~ 180 € | [MikroTik official](https://mikrotik.com/product/crs310_8g_2s_in) · [Amazon](https://www.amazon.de/s?k=MikroTik+CRS310-8G%2B2S%2BIN) |

### Why this switch and not a cheap unmanaged 2.5G switch?

Kubernetes is not just about port speed. The nodes constantly talk to each other — for pod networking, Longhorn replication, databases and message brokers. If all that cluster traffic has to travel through your home router, you lose all the benefits of 2.5G immediately. The MikroTik solves this with **Layer 3 routing**: it routes IP traffic directly between the nodes without a single packet ever leaving the switch to hit the router.

RouterOS 7 comes with a GUI, CLI and REST API. That means you can build traffic dashboards, set alerts, manage the entire network config as code and experiment with VLANs for cleaner network separation. The two SFP+ ports also leave room to grow: a faster uplink, a NAS connection or a second switch can be added later without replacing the core hardware.

If you already have a fast router with Layer 3 features you could use a cheaper unmanaged switch instead — but then all of the above goes away.

### Maxed Switch Setup
All traffic — data and management — runs through the MikroTik. Works up to 4 nodes before all 8× 2.5G RJ45 ports are occupied. The two SFP+ ports remain free for a WiFi AP and Node 5 without dual cable,
if a 5th Node is sat up then there is no room a NAS or future expansion.

```
[  Node 1  ]──  2.5G M.2  ──┐
[  Node 1  ]── 1G onboard ──┤
[  Node 2  ]──  2.5G M.2  ──┤
[  Node 2  ]── 1G onboard ──┤
[  Node 3  ]──  2.5G M.2  ──┤
[  Node 3  ]── 1G onboard ──┤── MikroTik CRS310 ──── Router (WAN only)
[  Node 4  ]──  2.5G M.2  ──┤
[  Node 4  ]── 1G onboard ──┤
[  Node 5  ]──   10G SFP+ ──┤
[   WiFi   ]──   10G SFP+ ──┘
```

---
 
## Patch Panel: HB-Digital 12-Port Cat.6a 10" 1HE
 
A clean build needs a clean cable termination point. Instead of plugging patch cables directly into the switch, all node cables terminate at the patch panel first. From there, short 0.25m slim patch cables run to the switch ports — keeping the cable routing tidy and making it easy to move, relabel or replace connections without touching the longer runs.
 
| Part | Details | Price | Where to find it |
|---|---|---:|---|
| HB-Digital 12-Port Patchpanel Cat.6a | 10" 1HE, STP, schwarz, 12× Cat.6a Keystone included | 35.90 € | [hb-digital.de](https://www.hb-digital.de/Patchpanel-12-Port-mit-Cat6a-RJ45-Keystone-Module-10-Patchfeld-1HE-schwarz) |
 
The 10" format matches the 3D-printed 1U rack mount used for the Tiny nodes. The Cat.6a Keystone modules are included and clip in tool-less via LSA snap-in — no crimping needed. With 12 ports there is enough room for the current 3-node dual-cable setup (6 ports used) and space to grow.
 
---
 
## Patch Cables — 0.25m Slim
 
Short slim patch cables connect the patch panel front to the switch ports directly beside it. Keeping these as short as possible is what makes the dual-cable layout look intentional rather than chaotic.
 
| Part | Details | Price | Where to find it |
|---|---|---:|---|
| 0.25m Slim Patch Cable Cat.6 | Short run from patch panel to switch, per cable | ~ 1.50–2.50 € | [Amazon](https://www.amazon.de/s?k=0.25m+patchkabel+slim+cat6) |
 
For the current 3-node setup with dual cables: 6 node connections + 1 router uplink = **7 cables minimum**. Buying 10 leaves a few spares for future nodes or replacements.

---

## Management Extension: Netgear GS308 *(When scaling horizontally)*

Not purchased yet — planned for a later stage when a dedicated management network becomes necessary.

| Part | Details | Price | Where to find it |
|---|---|---:|---|
| Netgear GS308 | 8× 1G unmanaged | current market price | [Amazon](https://www.amazon.de/NETGEAR-GS308-300PES-Netgear-neu/dp/B07PTTX7MX) |

The GS308 would serve as a simple 1G extension switch. Its only job is to connect the onboard 1G ports of the Tiny nodes, providing a dedicated path for SSH, monitoring and fallback traffic. No routing or management features needed from it — the MikroTik handles all of that. The GS308 just extends the number of available 1G ports.

### Maxed Dual Switch Setup
Management traffic moves to a dedicated Netgear GS308, freeing all 8× 2.5G ports on the MikroTik for cluster data. Scales up to 7 nodes with a dedicated management path, plus Node 8 connecting via SFP+ for a faster dedicated link.

```
[       Node 1      ]──  2.5G M.2 ──┐
[       Node 2      ]──  2.5G M.2 ──┤
[       Node 3      ]──  2.5G M.2 ──┤
[       Node 4      ]──  2.5G M.2 ──┤
[       Node 5      ]──  2.5G M.2 ──┤
[       Node 6      ]──  2.5G M.2 ──┤── MikroTik CRS310 ──── Router (WAN only)
[       Node 7      ]──  2.5G M.2 ──┤
[       Node 8      ]──  2.5G M.2 ──┤
[  MikroTik CRS310  ]──  10G SFP+ ──┤
[        WiFi       ]──  10G SFP+ ──┘

[      Node 1     ]── 1G onboard ──┐
[      Node 2     ]── 1G onboard ──┤
[      Node 3     ]── 1G onboard ──┤
[      Node 4     ]── 1G onboard ──┤── Netgear GS308 ──── MikroTik (VLAN trunk)
[      Node 5     ]── 1G onboard ──┤
[      Node 6     ]── 1G onboard ──┤
[      Node 7     ]── 1G onboard ──┤
[ MikroTik CRS310 ]── 1G onboard ──┘
```

The 2.5G link handles all Kubernetes and storage traffic. The 1G link handles management, SSH, monitoring and fallback. The Netgear switch connects to the MikroTik via a VLAN trunk — the MikroTik remains the single point for routing, VLAN assignment and internet access.

---

## Upgrade Path

**Mid term**
- Purchase and set up the Netgear GS308 once the management network separation becomes relevant
- Connect all onboard 1G ports to create the full dual-path setup

**Long term**
- Use the SFP+ ports on the MikroTik for a faster uplink or a dedicated NAS connection
- Add a second switch when expanding beyond 7 nodes