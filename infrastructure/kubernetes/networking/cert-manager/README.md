# cert-manager

[<- Back to Kubernetes Networking](../README.md)

cert-manager automates certificate creation, renewal and distribution inside Kubernetes.

It can issue certificates from public authorities such as Let's Encrypt or from an internal CA.

TLS certificates are what allow HTTPS clients to verify that they are talking to the expected service and to encrypt traffic. Without automation, certificates must be requested, installed, renewed and replaced manually.

cert-manager brings that lifecycle into Kubernetes. An operator creates Kubernetes resources such as `Certificate` and `Issuer`, and cert-manager requests or signs the certificate, stores it in a Kubernetes Secret and renews it before it expires.

For beginners, the practical result is simple: instead of manually copying certificate files into Traefik or application pods, the cluster can manage certificates declaratively.

---

## Why It Fits

TLS should be normal, even in a homelab. cert-manager removes manual certificate handling and makes HTTPS reproducible through Kubernetes resources.

It also connects several important concepts: DNS names, ingress routing, Let's Encrypt, internal certificate authorities, Kubernetes Secrets and certificate renewal. Those concepts appear constantly in production infrastructure.

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

cert-manager is currently `⚫ Inactive`. It should run permanently once TLS is used by cluster services.

---

## Future Deployment Link

Planned deployment location:

```text
../../../../helm-charts/networking/cert-manager/
```

---

## Learning Links

- [cert-manager documentation](https://cert-manager.io/docs/)
- [Let's Encrypt documentation](https://letsencrypt.org/docs/)
- [Wikipedia: Public key certificate](https://en.wikipedia.org/wiki/Public_key_certificate)
- [Wikipedia: Transport Layer Security](https://en.wikipedia.org/wiki/Transport_Layer_Security)
