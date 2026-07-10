# DuckDNS

[<- Back to DNS](../README.md)

DuckDNS is a free dynamic DNS service: it gives you a public subdomain (`yourname.duckdns.org`) that always points at your home IP address, even when the ISP changes it.

In this homelab, DuckDNS is **part of the chosen stack**: it provides the free, always-current public name for entry points that need one — for example the public reachability of a self-hosted [NetBird](../../ingress/netbird) server — while the Cloudflare-managed domain (see [Cloudflare Tunnel](../../ingress/cloudflare-tunnel)) covers the user-facing app names. For readers who own no domain at all, DuckDNS alone is also the free entry path into remote access.

Dynamic DNS exists because most home connections have changing IP addresses. A small updater — a cron job or Kubernetes CronJob calling the DuckDNS token API — reports the current IP every few minutes, and the DNS record follows. Combined with a router port forward, services become reachable at a stable name; combined with a DNS-01 webhook, even Let's Encrypt certificates work without any open port.

---

## Why It Fits

DuckDNS earns its place in the stack:

- it is the classic zero-cost answer to "how do I reach my homelab from outside?"
- it teaches the dynamic-DNS concept that also underlies paid DynDNS offerings
- cert-manager can issue real TLS certificates for `*.duckdns.org` names via a community DNS-01 webhook — free valid HTTPS without a domain
- it is the natural stepping stone before buying a domain and moving to Cloudflare or deSEC

Its role here is deliberately narrow: a free, stable name for the few entry points that need direct reachability. User-facing apps get real names on the owned Cloudflare domain; DuckDNS covers the plumbing underneath and costs nothing.

---

## Used For

- a stable public name for a changing home IP
- first remote access experiments with router port forwarding
- Let's Encrypt certificates via DNS-01 webhook (no open ports needed)
- learning how dynamic DNS updaters work (a one-line cron job)

---

## Strengths

- Completely free, up to five subdomains per account.
- Dead-simple token API; the updater is a single `curl` call.
- Community cert-manager webhook enables DNS-01 challenges.
- No client software required — any device that can run cron works.

---

## Weaknesses

- Free community service: no SLA, occasional slowness or outages.
- Only subdomains of `duckdns.org` — no own domain, no vanity names.
- Used with port forwarding, it exposes the home IP directly (the opposite of the tunnel/mesh approach this homelab targets).
- Single-purpose: no zone management, no mail records, no delegation.

---

## Infrastructure Dependencies

The planned shape here (and the typical homelab shape):

| Dependency | Purpose |
|---|---|
| Kubernetes CronJob (or router feature) | Periodic IP update against the DuckDNS API |
| [`../../ingress/cert-manager`](../../ingress/cert-manager) | TLS via the community DuckDNS DNS-01 webhook |
| [`../../../../setup/networking`](../../../../setup/networking) | Router port forward, if direct exposure is intended |

---

## Comparison Notes

| System | Best at | Tradeoff |
|---|---|---|
| DuckDNS | Free, instant, zero setup | Subdomain only, no guarantees |
| Own domain + Cloudflare | Full control, tunnel support, real DNS | Costs a domain (~10 €/year) |
| dynv6 / deSEC | Free dynamic DNS with more DNS features | Smaller communities |
| No-IP / DynDNS | Long-established commercial DynDNS | Free tiers with renewal nagging |

The short version: DuckDNS for free plumbing names and as the everything-for-zero-cost entry path; the owned Cloudflare domain for user-facing app names. This repository uses both, each for its layer.

---

## Runtime Status

DuckDNS is currently `⚫ Inactive`. It is part of the chosen access stack and becomes active together with the first externally reachable entry point (typically alongside NetBird).

---

## Future Deployment Link

The updater CronJob will live at:

```text
../../../../helm-charts/infrastructure/platform/dns/duckdns/
```

---

## Documentation

- [DuckDNS](https://www.duckdns.org/)
- [DuckDNS install/updater examples](https://www.duckdns.org/install.jsp)
- [cert-manager webhook for DuckDNS (community)](https://github.com/ebrianne/cert-manager-webhook-duckdns)
- [Wikipedia: Dynamic DNS](https://en.wikipedia.org/wiki/Dynamic_DNS)
