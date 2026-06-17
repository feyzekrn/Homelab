# cert-manager

[<- Back to Kubernetes Networking](../README.md)

cert-manager automates certificate creation, renewal and distribution inside Kubernetes.

It can issue certificates from public authorities such as Let's Encrypt or from an internal CA.

---

## Why It Fits

TLS should be normal, even in a homelab. cert-manager removes manual certificate handling and makes HTTPS reproducible through Kubernetes resources.

---

## Used For

- ingress TLS certificates
- internal service certificates
- future mTLS experiments
- certificate renewal automation

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
