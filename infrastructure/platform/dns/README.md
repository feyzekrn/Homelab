# DNS

[<- Back to Platform](../README.md)

This directory documents DNS for the homelab: how names are resolved inside the cluster, inside the LAN and for people using the network every day.

DNS is the system that translates names such as `grafana.homelab.local` into IP addresses. Every other networking component in this catalog depends on it. Ingress rules are name-based, TLS certificates are issued for names, and humans remember names, not IP addresses.

For this homelab, DNS is split into three different jobs that are easy to confuse:

- **Cluster DNS**: pods resolving Kubernetes Service names such as `postgresql.databases.svc.cluster.local`. Kubernetes ships CoreDNS for this out of the box.
- **Internal LAN DNS**: laptops, phones and other LAN devices resolving homelab names such as `nextcloud.home.example.com` to the MetalLB/Traefik IPs.
- **Filtering/forwarding DNS**: the resolver the whole household actually uses, which can also block ads, trackers and malware domains before forwarding everything else upstream.

One tool rarely does all three jobs well. This project uses CoreDNS for cluster and internal zones and AdGuard Home as the LAN-facing filtering resolver. Pi-hole is documented as the most popular alternative for the filtering role.

---

## Why This Matters

Without homelab DNS, every service is reached by IP address and port. That breaks TLS, makes ingress routing pointless and turns the network into a list of numbers nobody remembers. With DNS, the platform gets stable names, per-service certificates and clean URLs on every device in the house.

In a homelab, running your own resolver also removes a hidden dependency: by default every device asks the ISP or router for DNS. Hosting DNS yourself teaches how resolution, forwarding, caching and authoritative zones actually work — and it gives network-wide ad blocking for free.

In companies, DNS is one of the most critical shared services. Split-horizon DNS, internal zones, resolver redundancy and DNS-based service discovery are everyday production concerns. The homelab version is smaller but teaches the same failure modes, including the most famous one: when DNS is down, everything looks down.

---

## What You Can Do With It

- give every homelab service a real name
- resolve internal zones that do not exist on the public internet
- block ads and trackers for every device on the LAN
- keep working when the internet connection is flaky (caching)
- issue TLS certificates for internal names
- learn the difference between recursive, forwarding and authoritative DNS
- understand why Kubernetes ships its own DNS server

---

## Roles And Components

| Role | Question it answers | Component |
|---|---|---|
| Cluster DNS | How do pods resolve Service names? | [`./coredns`](./coredns) |
| Internal zones | How does `*.home.example.com` resolve on the LAN? | [`./coredns`](./coredns) or AdGuard Home DNS rewrites |
| Filtering resolver | Which DNS server do household devices use? | [`./adguard-home`](./adguard-home) |
| Filtering alternative | What is the classic homelab choice for this? | [`./pihole`](./pihole) |
| DHCP handout | How do devices learn which resolver to use? | [`../../../setup/networking`](../../../setup/networking) (MikroTik DHCP) |

---

## Component Catalog

| Name | Path | Status | Recommendation | Purpose |
|---|---|---|---|---|
| CoreDNS | [docs](./coredns) · [chart](../../../helm-charts/infrastructure/platform/dns/coredns) · [config](./coredns/terraform) | ⚫ Inactive | Cluster standard, also good for internal zones | Cluster DNS and authoritative internal DNS |
| AdGuard Home | [docs](./adguard-home) · [chart](../../../helm-charts/infrastructure/platform/dns/adguard-home) · [config](./adguard-home/terraform) | ⚫ Inactive | Chosen LAN resolver for this homelab | Network-wide filtering and forwarding resolver |
| Pi-hole | [docs](./pihole) | ⚫ Inactive | Documented alternative | Classic network-wide ad-blocking resolver |

---

## Planned Resolution Flow

The target design for this homelab:

1. MikroTik DHCP hands out AdGuard Home as the DNS server for all LAN devices.
2. AdGuard Home filters ads/trackers and answers from cache when possible.
3. Queries for internal homelab zones are forwarded to CoreDNS, which is authoritative for them.
4. All other queries are forwarded to a public upstream, preferably over an encrypted transport (DNS-over-TLS or DNS-over-HTTPS).
5. Inside the cluster, pods keep using the Kubernetes-managed CoreDNS as usual — the LAN setup does not replace it.

---

## Operational Warning

DNS is the one homelab service that affects people who did not sign up for a homelab. If the resolver runs on the cluster and the cluster is down, the whole household loses the internet as far as they can tell.

Mitigations to plan before making homelab DNS the household default:

- configure a second DNS server in DHCP (a second resolver instance or a public fallback)
- prefer running the LAN resolver with a stable MetalLB IP, not behind ingress
- consider whether the resolver should even run on the cluster, or on a small always-on host
- test what happens during cluster upgrades before the family depends on it

---

## Deployment Rule

Documentation lives here. Deployment assets should live under:

```text
../../../helm-charts/infrastructure/platform/dns/<component>/
```

---

## Learning Links

- [Wikipedia: Domain Name System](https://en.wikipedia.org/wiki/Domain_Name_System)
- [Wikipedia: Name server](https://en.wikipedia.org/wiki/Name_server)
- [Kubernetes DNS documentation](https://kubernetes.io/docs/concepts/services-networking/dns-pod-service/)
- [Wikipedia: DNS over HTTPS](https://en.wikipedia.org/wiki/DNS_over_HTTPS)
- [Wikipedia: Split-horizon DNS](https://en.wikipedia.org/wiki/Split-horizon_DNS)
