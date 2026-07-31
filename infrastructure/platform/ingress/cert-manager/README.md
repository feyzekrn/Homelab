# cert-manager

[<- Back to Ingress](../README.md)

cert-manager automates certificate creation, renewal and distribution inside Kubernetes (`k8s`).

It can issue certificates from public authorities such as Let's Encrypt or from an internal CA.

**It covers the cluster half of TLS only.** The Proxmox world does not use it: [Caddy](../caddy) obtains and renews its own certificates automatically, which is one of the reasons it was chosen there. Two worlds, two certificate stories, no shared dependency — see the [ingress overview](../README.md#components).

TLS certificates are what allow HTTPS clients to verify that they are talking to the expected service and to encrypt traffic. Without automation, certificates must be requested, installed, renewed and replaced manually.

cert-manager brings that lifecycle into Kubernetes. An operator creates Kubernetes resources such as `Certificate` and `Issuer`, and cert-manager requests or signs the certificate, stores it in a Kubernetes Secret and renews it before it expires.

For beginners, the practical result is simple: instead of manually copying certificate files into Traefik or application pods, the cluster can manage certificates declaratively.

---

## Why It Fits

TLS should be normal, even in a homelab. cert-manager removes manual certificate handling and makes HTTPS reproducible through Kubernetes resources.

It also connects several important concepts: DNS names, ingress routing, Let's Encrypt, internal certificate authorities, Kubernetes Secrets and certificate renewal. Those concepts appear constantly in production infrastructure.

---

## Prerequisites

| Requirement | Why |
|---|---|
| A running cluster with [Cilium](../../../kubernetes/cilium) | It runs as pods and needs to reach the ACME endpoint |
| **An own domain** | Let's Encrypt does not issue for made-up internal TLDs |
| A **Cloudflare API token** | For DNS-01 challenges — the issuer writes a TXT record to prove domain control |
| [Traefik](../traefik) | The consumer: cert-manager fills a Secret, Traefik serves it |
| [Vault](../../security/secret-store) + [External Secrets](../../security/external-secrets) | The API token must not be committed to Git |

**Use DNS-01, not HTTP-01.** The HTTP-01 challenge requires Let's Encrypt to reach the cluster from the internet on port 80, which this architecture deliberately does not allow — there are no inbound ports and no port forwarding anywhere in the design. DNS-01 proves domain ownership through a TXT record instead, works entirely outbound, and has the additional benefit of supporting **wildcard certificates**.

This is the same mechanism [Caddy](../caddy) uses on the Proxmox side, for the same reason.

---

## Used For

- ingress TLS certificates
- internal service certificates
- future mTLS experiments
- certificate renewal automation
- testing public and private certificate authority workflows

---

## Strengths

- Automates a repetitive and error-prone operational task.
- Fits GitOps because certificate intent is described as Kubernetes resources.
- Supports public issuers such as Let's Encrypt and internal CA workflows.
- Reduces outage risk from forgotten certificate expiry.
- Works well with ingress controllers such as Traefik and ingress-nginx.

---

## Weaknesses

- DNS and issuer configuration must be correct before automation works.
- Public certificate issuance can hit rate limits during repeated experiments.
- Private CAs require clients to trust the internal root certificate.
- It manages certificates, not application authentication or authorization.

---

## Alternatives

| Alternative | Notes |
|---|---|
| Manual certificates | Fine for quick tests, bad for repeatability |
| Step CA | Strong internal CA option, can work with cert-manager |
| External reverse proxy certificates | Works, but moves state outside Kubernetes |

---

## Runtime Status

cert-manager is currently `⚫ Inactive`. It is deployed together with [Traefik](../traefik) — the first exposed cluster service needs both, and configuring the ingress controller without TLS only means doing the work twice.

**Use the Let's Encrypt staging issuer first.** Production has rate limits that are easy to hit while a DNS-01 configuration is still wrong, and a week-long lockout at that stage is a genuinely annoying way to learn. Switch the issuer to production once a staging certificate has been issued successfully.

---

## Future Deployment Link

Planned deployment location:

```text
../../../../helm-charts/infrastructure/platform/ingress/cert-manager/
```

---

## Learning Links

- [cert-manager documentation](https://cert-manager.io/docs/)
- [Let's Encrypt documentation](https://letsencrypt.org/docs/)
- [Wikipedia: Public key certificate](https://en.wikipedia.org/wiki/Public_key_certificate)
- [Wikipedia: Transport Layer Security](https://en.wikipedia.org/wiki/Transport_Layer_Security)
