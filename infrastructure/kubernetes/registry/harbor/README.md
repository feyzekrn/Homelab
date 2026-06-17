# Harbor

[<- Back to Container Registry](../README.md)

Harbor is a full-featured container registry with projects, access control, vulnerability scanning and image retention policies.

---

## Why It Fits

Harbor is useful once the homelab builds and runs multiple custom images. It teaches registry operations beyond simply pushing images to a public service.

---

## Used For

- hosting internal container images
- image retention policies
- vulnerability scanning experiments
- project-level access control

---

## Alternatives

| Alternative | Notes |
|---|---|
| GitHub Container Registry | Simple and good enough for many projects |
| Docker Hub | Common but rate limits and public defaults matter |
| Plain registry:2 | Lightweight, fewer platform features |

---

## Runtime Status

Harbor is currently `⚫ Inactive`. Start with an external registry unless self-hosting images becomes a learning goal.

---

## Future Deployment Link

Planned deployment location:

```text
../../../../helm-charts/registry/harbor/
```
