# CoreDNS

[<- Back to DNS](../README.md)

CoreDNS is a flexible, plugin-based DNS server written in Go. It is the default cluster DNS in Kubernetes and can also act as an authoritative or forwarding DNS server for a LAN.

In this homelab, CoreDNS appears in two roles that should not be confused:

- **Cluster DNS**: every Kubernetes cluster already runs CoreDNS. Pods use it to resolve Service names such as `redis.databases.svc.cluster.local`. This instance is installed by the cluster bootstrap and normally should not be touched.
- **Internal zone DNS**: a second, separately deployed CoreDNS instance can be authoritative for homelab zones such as `home.example.com`, answering queries forwarded from AdGuard Home.

CoreDNS is configured through a single `Corefile` where behavior is composed from plugins: serve this zone from a file, forward that zone upstream, cache answers, export Prometheus metrics. That plugin model is why the same binary works as cluster DNS, LAN DNS or ad-hoc forwarder.

---

## Why It Fits

CoreDNS is a natural fit because it is already in the cluster and because learning it pays off twice:

- it explains how Kubernetes service discovery actually works
- it is a realistic authoritative DNS server for internal zones
- the `Corefile` teaches DNS concepts (zones, forwarding, caching) explicitly
- it exports Prometheus metrics out of the box
- it is lightweight enough to run anywhere

Understanding CoreDNS also demystifies a whole class of cluster problems: failed service discovery, `ndots` issues and slow lookups all pass through it.

---

## Used For

- resolving Kubernetes Service names inside the cluster
- serving authoritative internal homelab zones
- forwarding selected zones to other resolvers
- caching DNS answers
- learning DNS server configuration hands-on
- monitoring DNS query behavior with Prometheus metrics

---

## Strengths

- Kubernetes standard, so the knowledge is directly reusable.
- Plugin architecture keeps configuration explicit and composable.
- Very light on resources.
- Good observability through Prometheus metrics.
- Single binary, easy to run in or outside Kubernetes.

---

## Weaknesses

- No web UI; configuration is file-based only.
- No built-in ad/tracker blocking (that is AdGuard Home's job here).
- Zone files must be managed by hand or through automation.
- The double role (cluster DNS vs. LAN DNS) confuses beginners if not clearly separated.

---

## Infrastructure Dependencies

| Dependency | Purpose |
|---|---|
| [`../../metallb`](../../metallb) | Stable LAN IP for a LAN-facing CoreDNS instance |
| [`../../cilium`](../../cilium) | Pod networking for the cluster DNS role |
| [`../../../observability/metrics/prometheus`](../../../observability/metrics/prometheus) | Scraping CoreDNS metrics |
| [`../../../../network`](../../../../network) | DHCP/router integration so clients can reach the resolver |

---

## Application Examples

- Serve `home.example.com` as an authoritative zone with records pointing at Traefik.
- Receive forwarded internal-zone queries from AdGuard Home.
- Inspect cluster DNS behavior when a pod cannot resolve a Service name.
- Watch cache hit rates and query types in Grafana.

---

## Comparison Notes

| System | Best at | Tradeoff |
|---|---|---|
| CoreDNS | Kubernetes-native, composable plugin config | No UI, no filtering |
| BIND | The reference authoritative DNS server | Heavy configuration, steep learning curve |
| Unbound | Validating recursive resolver | Not aimed at authoritative zones |
| dnsmasq | Tiny DNS+DHCP for small networks | Less structured for growing setups |
| Technitium | Full DNS server with web UI | Smaller community, less Kubernetes-idiomatic |

---

## Hands-On Start

Deployment files should eventually live under `helm-charts`.

First evaluation checklist:

1. Inspect the existing cluster CoreDNS: `kubectl -n kube-system get configmap coredns -o yaml`.
2. Deploy a second CoreDNS instance with its own `Corefile` and an internal test zone.
3. Expose it on a stable MetalLB IP.
4. Point AdGuard Home (or `dig @<ip>`) at it and resolve a test record.
5. Add the Prometheus plugin and check metrics in Grafana.
6. Only then make real internal zones authoritative.

---

## Runtime Status

CoreDNS as cluster DNS will be `🟢 Active` automatically once the cluster exists. The LAN-facing internal-zone instance is currently `⚫ Inactive`.

---

## Future Deployment Link

Planned deployment location:

```text
../../../../../helm-charts/networking/dns/coredns/
```

---

## Documentation

- [CoreDNS documentation](https://coredns.io/manual/toc/)
- [CoreDNS plugins](https://coredns.io/plugins/)
- [Kubernetes: Customizing DNS](https://kubernetes.io/docs/tasks/administer-cluster/dns-custom-nameservers/)
- [Wikipedia: CoreDNS](https://en.wikipedia.org/wiki/CoreDNS)
