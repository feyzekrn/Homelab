# AdGuard Home

[<- Back to DNS](../README.md)

AdGuard Home is a network-wide DNS resolver with built-in ad, tracker and malware-domain blocking, configured through a modern web UI.

In this homelab, AdGuard Home is the **chosen LAN-facing resolver**: the DNS server that all household devices receive via DHCP. It filters unwanted domains, caches answers, forwards internal homelab zones to CoreDNS and sends everything else to an encrypted public upstream.

**It runs in both worlds** (`lxc + k8s`): the primary instance is a container on [`pve0`](../../../../setup/compute/proxmox-cluster), with a replica on the cluster later — two independent resolvers built from one config file, see [keeping both instances in sync](#keeping-both-instances-in-sync). The primary belongs on the Proxmox side because DNS serves the entire household — an outage is not "a service is down", it is "the internet is broken" for everyone in the flat, and that must not depend on the experimentation field.

---

## Prerequisites

| Requirement | Why |
|---|---|
| Proxmox VE running | The primary is an LXC — that is all it needs |
| A static IP | Clients get this address by DHCP; it cannot move |
| Control over DHCP | Fritz!Box now, [OPNsense](../../../../setup/networking/router/opnsense) later, to hand out the resolver |
| [CoreDNS](../coredns) | Only for internal zone forwarding — optional at first |
| [MetalLB](../../../kubernetes/metallb) | **Only for the `k8s` replica**, which comes much later |

**Nothing here waits for the cluster.** The primary instance runs on the current flat network, which makes it the earliest component in this repository that delivers visible everyday value.

It works at the DNS level: when a device asks for a known ad or tracking domain, AdGuard Home answers with a blocked response instead of the real IP. Every device on the network benefits — phones, TVs, consoles — without installing anything on them.

---

## Why It Fits

AdGuard Home was chosen over Pi-hole for this project because:

- encrypted upstreams (DNS-over-HTTPS/TLS/QUIC) are built in, no extra sidecar needed
- it can also *serve* encrypted DNS to clients, useful for phones outside the LAN
- per-client settings and parental controls fit the multi-user family goal
- DNS rewrites for internal names are a first-class UI feature
- single Go binary, easy to run in Kubernetes
- configuration lives in one YAML file, which suits a GitOps mindset

It is also a genuinely useful always-on service: the first component where the family notices the homelab exists — in a good way.

---

## Used For

- network-wide ad and tracker blocking
- the default DNS resolver handed out by DHCP
- forwarding internal zones to CoreDNS
- encrypted DNS upstreams (DoH/DoT)
- per-device filtering rules and safe search for kids' devices
- DNS query statistics and debugging

---

## Strengths

- Modern UI with per-client configuration.
- Native encrypted DNS on both the client and upstream side.
- Built-in DNS rewrites for internal homelab names.
- Single binary with one config file; container-friendly.
- Actively developed by the AdGuard team.

---

## Weaknesses

- Smaller community than Pi-hole; fewer third-party guides.
- DNS-level blocking cannot remove ads served from first-party domains (e.g. YouTube).
- Becomes household-critical: outages affect everyone immediately.
- Statistics/query log grow and should be bounded on small volumes.
- Backed by a company with commercial products (the Home component itself is open source).

---

## Infrastructure Dependencies

| Dependency | Purpose |
|---|---|
| [`metallb`](../../../kubernetes/metallb) | Stable LAN IP — DNS clients need a fixed address, not ingress |
| [`coredns`](../coredns) | Upstream for internal homelab zones |
| [`longhorn`](../../storage/longhorn) | Persistence for config, filters and query log |
| [`networking`](../../../../setup/networking) | MikroTik DHCP must hand out the AdGuard IP |
| [`traefik`](../../ingress/traefik) | Optional HTTPS exposure of the admin UI only |

---

## Application Examples

- Hand out AdGuard Home as primary DNS via MikroTik DHCP.
- Rewrite `*.home.example.com` to the Traefik LoadBalancer IP.
- Give a child's tablet a stricter filtering profile than adult devices.
- Use the query log to find which device is phoning home at 3 a.m.
- Forward everything else to a DoH upstream so the ISP sees no plain-text DNS.

---

## Comparison Notes

| System | Best at | Tradeoff |
|---|---|---|
| AdGuard Home | Modern UI, encrypted DNS, per-client rules | Smaller ecosystem than Pi-hole |
| [Pi-hole](../pihole) | Huge community, classic homelab standard | Encrypted upstreams need extra components |
| Blocky | Lightweight, config-file-only blocker | No UI at all |
| NextDNS | Managed cloud filtering | Not self-hosted, subscription limits |

---

## Keeping Both Instances in Sync

Stated plainly, because the phrase "synced replica" above suggests otherwise: **AdGuard Home has no clustering.** No shared backend, no leader election, no replication. The LXC primary and the `k8s` replica are two entirely independent resolvers that happen to be configured the same way. Whatever keeps them aligned has to be added from outside.

Two ways to do that:

| Approach | How it works | Cost |
|---|---|---|
| [AdGuardHome-Sync](https://github.com/bakito/adguardhome-sync) | A small service copies the config from the primary to the replica through AdGuard's API, on a schedule | One more always-on component; the primary's UI stays the source of truth |
| **Git as the single source** | One `AdGuardHome.yaml` in this repository, rolled out to the LXC by [`ansible`](../../../provisioning/ansible) and to the cluster by [`flux`](../../../kubernetes/gitops/flux) | Nothing syncs at runtime; the UI becomes read-only in practice |

**Chosen: Git as the single source.** It is the same decision the rest of this repository makes — the description lives in version control, the running thing is derived from it. It also avoids a runtime dependency whose only job is to repair drift that would not exist if both copies came from one file. The tradeoff is real and worth naming: changes made by clicking in the AdGuard UI are no longer authoritative, and a change made there is lost on the next rollout.

**What never syncs, either way:** the query log, the statistics and per-instance TLS material. Those are local observations, not configuration — there is nothing to merge and no reason to try.

**Sync is not failover.** Two identically configured resolvers do not help while nothing switches the clients between them. The Fritz!Box hands out exactly one local DNS server and has no field for a second, so during the interim phase the fallback is manual: clear that field and the household resolves through the router again. Real failover needs either [OPNsense](../../../../setup/networking/router/opnsense) as the DHCP server, handing out two resolvers, or a shared VIP in front of both — both far later than the replica itself.

> ⚠️ `AdGuardHome.yaml` contains the admin password hash and, depending on the upstream, credentials. It belongs in this repository encrypted (`sops`/`age` or `ansible-vault`), never in plain text.

---

## Hands-On Start

Deployment files should eventually live under `helm-charts`.

First evaluation checklist:

1. Deploy with a persistent volume and a MetalLB service on TCP/UDP 53.
2. Point a single test device at it manually before touching DHCP.
3. Configure encrypted upstreams and enable the default blocklists.
4. Add DNS rewrites (or conditional forwarding to CoreDNS) for internal zones.
5. Verify blocking works, then update MikroTik DHCP for the whole LAN.
6. Configure a fallback DNS in DHCP before the family depends on it.

---

## Runtime Status

AdGuard Home is currently `⚫ Inactive`. It is **one of the first services in the whole homelab** — the primary instance is an LXC on [`pve0`](../../../../setup/compute/proxmox-cluster) and needs neither the cluster nor MetalLB, so it can run today on the flat interim network.

That makes it the earliest component that delivers visible household value: network-wide ad and tracker blocking, before a single Kubernetes node exists.

The `k8s` replica comes much later and is a convenience, not a requirement — it needs MetalLB for a stable service IP and exists so DNS survives `pve0` being rebooted for maintenance.

**One rule when it goes live:** DNS is the service whose outage looks like "the internet is broken" to everyone in the house. Hand it out via DHCP only after it has resolved reliably for a day, and keep a second resolver in the DHCP handout.

---

## Future Deployment Link

Planned deployment location:

```text
../../../../helm-charts/infrastructure/platform/dns/adguard-home/
```

---

## Documentation

- [AdGuard Home documentation](https://github.com/AdguardTeam/AdGuardHome/wiki)
- [AdGuard Home GitHub](https://github.com/AdguardTeam/AdGuardHome)
- [AdGuardHome-Sync](https://github.com/bakito/adguardhome-sync) — the API-based alternative to the chosen Git-as-source approach
- [Wikipedia: AdGuard](https://en.wikipedia.org/wiki/AdGuard)
- [Wikipedia: DNS sinkhole](https://en.wikipedia.org/wiki/DNS_sinkhole)
