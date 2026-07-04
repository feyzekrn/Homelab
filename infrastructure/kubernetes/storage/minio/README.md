# MinIO

[<- Back to Kubernetes Storage](../README.md)

MinIO provides S3-compatible object storage.

It is useful for applications that expect S3, for backup targets and for learning object storage patterns without using a public cloud provider.

Object storage stores data as objects inside buckets. Applications access those objects through an API instead of mounting a disk. This is the model popularized by Amazon S3, and many modern applications know how to talk to S3-compatible storage.

MinIO provides that kind of API in a self-hosted form. A service can upload a file to a bucket, read it later through an object key and manage access through credentials and bucket policies.

Object storage is different from block storage. A database usually wants block storage. Backups, artifacts, exports and file uploads often fit object storage better.

---

## Why It Fits

MinIO is the recommended homelab S3 equivalent. It gives applications an S3-compatible endpoint without requiring AWS, and it is easy to understand compared to larger distributed object-storage platforms.

For this project, MinIO is the first choice for self-hosted buckets, backup targets and local development against S3 APIs.

---

## Used For

- application object storage
- backup targets
- artifact storage
- S3-compatible development and testing
- storing uploads from services
- testing S3 SDK integrations

---

## Strengths

- Strong S3-compatible API for self-hosted environments.
- Useful for Velero-style backup targets and application uploads.
- Easier to reason about than larger object-storage platforms.
- Good local development substitute for cloud S3.
- Integrates with many SDKs and tools that already support S3.

---

## Weaknesses

- It is not a POSIX filesystem replacement.
- Bucket policies and credentials still need security design.
- Distributed production-style MinIO requires careful disk and node planning.
- It should not be treated as the only backup location if it runs in the same failure domain as the cluster.

---

## Application Examples

- A dashboard stores exported reports in a private bucket.
- Velero or another backup tool writes backups to an S3-compatible target.
- A service stores user-uploaded files without putting them into PostgreSQL.
- CI publishes generated artifacts into a bucket.
- Local development uses the same S3 API shape as production-style object storage.

---

## When To Run

MinIO is currently `⚫ Inactive`. It does not need to run from day one. Add it when an application, backup workflow or artifact workflow needs object storage.

---

## Alternatives

| Alternative | Location | Homelab fit | Business fit | Notes |
|---|---|---|---|---|
| MinIO | Self-hosted | Recommended | Good for many private platforms | Strong S3 compatibility and simple operational model |
| Garage | Self-hosted | Good | Niche | Lightweight distributed object storage |
| SeaweedFS | Self-hosted | Advanced | Niche | Flexible, broad feature set |
| AWS S3 | External | Optional | Standard | Operationally simple, not self-hosted |
| Backblaze B2 | External | Optional | Good | S3-compatible hosted object storage |

---

## Hands-On Start

Deployment files should eventually live under `helm-charts`, but the basic upstream Helm flow is:

```bash
helm repo add minio https://charts.min.io/
helm repo update
helm install minio minio/minio --namespace minio --create-namespace
```

After installing, create a first bucket for test uploads and configure one application or backup tool against the S3 endpoint.

---

## Future Deployment Link

Planned deployment location:

```text
../../../../helm-charts/storage/minio/
```

---

## Documentation

- [MinIO documentation](https://min.io/docs/minio/kubernetes/upstream/)
- [MinIO JavaScript SDK](https://min.io/docs/minio/linux/developers/javascript/minio-javascript.html)
- [MinIO Go SDK](https://min.io/docs/minio/linux/developers/go/minio-go.html)
- [Wikipedia: MinIO](https://en.wikipedia.org/wiki/MinIO)
- [Wikipedia: Object storage](https://en.wikipedia.org/wiki/Object_storage)
