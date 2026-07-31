# Home Assistant

[← Back to Applications](../README.md)

Home Assistant is an open-source home automation platform: it talks to smart devices — lights, plugs, sensors, cameras, thermostats — over dozens of protocols, keeps their state locally, and runs automations on top of them. Unlike vendor apps, it works without a cloud account and without each manufacturer's own ecosystem.

In this homelab it is the **flagship cluster application**: the one user-facing app that genuinely belongs on Kubernetes rather than on the Proxmox host.

---

## Why It Runs On `k8s`

Every other family-facing app in this repository lands on the Proxmox host, because stability matters more than failover for photos and films. Home Assistant is the exception, and the reason is what happens when it is down:

- **It controls physical things.** Lights that do not switch, heating that does not adjust and alarms that do not fire are noticed immediately by everyone in the house — including the people who did not ask for a homelab.
- **Automations are time-sensitive.** A photo library can wait an hour for a host to come back. A motion-triggered light cannot.
- **It is stateless enough to move.** Its configuration and database live on a volume; the process itself can be rescheduled to another node without ceremony.

That combination — high perceived availability, low state complexity — is exactly the profile Kubernetes handles well. If a node dies, the cluster restarts Home Assistant elsewhere and the house keeps working.

---

## Its Place In The Network

Home Assistant is the one service that deliberately reaches into the **IoT VLAN**, and the direction of that access is the whole point of the zone design:

- **Allowed:** `k8s` → IoT — Home Assistant may talk to the plugs, sensors and lights.
- **Denied:** IoT → everything else, except the MQTT broker's address and port.

Cheap smart devices are the least trustworthy things on the network: old firmware, no updates, cloud dependencies. Penning them into their own VLAN and letting only Home Assistant initiate contact means a compromised plug reaches nothing at all — while automation still works normally.

MQTT, the protocol most sensors speak, is served by [NATS](../../infrastructure/platform/messaging/nats) in this homelab rather than a separate broker.

---

## Access From Outside

Home Assistant is the most security-sensitive application here — it controls the house, and publicly reachable instances are actively scanned. It is therefore **not exposed like the media apps are**:

1. **Default: no exposure at all.** Access from outside goes through [NetBird](../../infrastructure/platform/ingress/netbird), the same private path used for administration.
2. **If mobile access without VPN becomes necessary** (the companion app running in the background), it goes through a [Cloudflare Tunnel](../../infrastructure/platform/ingress/cloudflare-tunnel) with **Cloudflare Access in front** — an identity check at the edge, before a request ever reaches the tunnel.
3. **In the app itself:** two-factor authentication enabled and login rate limiting on.

The principle: the authentication hurdle belongs as far outside as possible, not at the application that controls the door locks.

---

## Prerequisites

| Requirement | Why |
|---|---|
| A running cluster with [Cilium](../../infrastructure/kubernetes/cilium) | It is the one family-facing app that is a cluster workload |
| [Longhorn](../../infrastructure/platform/storage/longhorn) | Its configuration and state have to survive rescheduling |
| [MetalLB](../../infrastructure/kubernetes/metallb) + [Traefik](../../infrastructure/platform/ingress/traefik) | Reachable under a hostname on the LAN |
| [NATS](../../infrastructure/platform/messaging/nats) | The MQTT broker its sensors speak to |
| **IoT VLAN (40) configured** | The zone model only works if the devices are actually penned into it |
| Firewall rule `k8s → IoT` | One-directional: Home Assistant may initiate, the devices may not |
| [NetBird](../../infrastructure/platform/ingress/netbird) | Access from outside — this app is not exposed publicly by default |

**The VLAN work is the real prerequisite**, and it is the one that needs hardware: the IoT zone requires the managed switch and [OPNsense](../../setup/networking/router/opnsense) as gateway. Home Assistant runs perfectly well on a flat network first — it just does not get the isolation that makes cheap smart devices acceptable on the network at all.

---

## Infrastructure Dependencies

| Dependency | Purpose |
|---|---|
| [`longhorn`](../../infrastructure/platform/storage/longhorn) | Persistent volume for configuration and the state database |
| [`postgresql`](../../infrastructure/platform/databases/postgresql) | Recorder database — the default SQLite does not enjoy being rescheduled |
| [`traefik`](../../infrastructure/platform/ingress/traefik) | Ingress inside the cluster |
| [`nats`](../../infrastructure/platform/messaging/nats) | MQTT broker for sensors and devices |
| [`netbird`](../../infrastructure/platform/ingress/netbird) | Private access from outside the LAN |
| [`velero`](../../infrastructure/platform/backup/velero) | Backup — automations represent real accumulated work |

---

## Known Friction

- **Device discovery does not cross VLANs.** Anything relying on mDNS or broadcast (Chromecast, HomeKit, some WiFi plugs) needs the mDNS repeater on [OPNsense](../../setup/networking/router/opnsense), or explicit IP configuration.
- **USB radios are awkward on Kubernetes.** Zigbee or Z-Wave sticks are physical devices attached to one machine — a pod cannot follow them across nodes. The clean solution is a network-attached coordinator (Zigbee2MQTT on a small always-on device), which keeps the cluster free of hardware pinning.
- **The recorder database grows.** Without a retention policy it will happily fill a volume with sensor history nobody reads.

---

## Runtime Status

`⚫ Inactive` — planned as one of the first real workloads once the cluster runs. It is also the reason several platform components exist: NATS, PostgreSQL and the IoT VLAN all have Home Assistant as their first consumer.

---

## Documentation

- [Home Assistant documentation](https://www.home-assistant.io/docs/)
- [Home Assistant on Kubernetes](https://www.home-assistant.io/installation/alternative/)
- [Wikipedia: Home Assistant](https://en.wikipedia.org/wiki/Home_Assistant)
