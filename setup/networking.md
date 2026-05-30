# 🔌 Networking — Switches & Physical Topology

[← Back to Setup Overview](./README.md)

---

## Core Switch: MikroTik CRS310-8G+2S+IN

The central switch for the whole cluster. Bought new, because this switch brings real features that actually matter for Kubernetes.

| Part | Details | Price | Where to find it |
|---|---|---:|---|
| MikroTik CRS310-8G+2S+IN | 8× 2.5G ports + 2× SFP+ | **~ €180** | [MikroTik official](https://mikrotik.com/product/crs310_8g_2s_in) · [Amazon](https://www.amazon.de/s?k=MikroTik+CRS310-8G%2B2S%2BIN) |

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

## Management Extension: Netgear GS308 *(Planned)*

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