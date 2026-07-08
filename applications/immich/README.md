# Immich

[<- Back to User-Facing Applications](../README.md)

Immich is a self-hosted photo and video management platform designed as a direct replacement for Google Photos and iCloud Photos.

In this homelab, Immich is the **planned family photo cloud**. Its mobile apps automatically back up photos and videos from iOS and Android in the background, the web UI provides timeline, search, albums and sharing, and machine-learning features (face recognition, object search) run entirely locally.

Immich is deliberately opinionated about one job: photos. Nextcloud can also store photos, but Immich's mobile backup, timeline performance and ML-powered search are in a different league — which is why this homelab runs both, with a clear split: [Nextcloud](../nextcloud) for files, calendars and contacts; Immich for the photo library.

---

## Why It Fits

Immich fits the "replace iCloud" goal precisely where it hurts most — photos:

- automatic background upload from every family phone, like iCloud Photos
- each user gets a private library; albums can be shared within the family
- partner sharing, shared albums and public links cover the family workflows
- face and object search without sending images to any cloud provider
- OAuth/OIDC login means [Keycloak](../../infrastructure/platform/security/rights-management/keycloak) accounts work here too

It is also an excellent platform test: Immich is a multi-service deployment (server, machine-learning service, PostgreSQL with vector extension, Redis) with real storage growth — much closer to a production application than a single-container app.

---

## Family And Multi-User Model

The intended setup mirrors the Nextcloud family model documented in [Nextcloud: Multi-User And Family Setup](../nextcloud/multi-user-family.md):

- every family member gets their own Keycloak identity and logs into Immich with it
- each user has a **private photo area** — uploads from their phone land only in their library
- **shared albums** collect vacations, birthdays and kids' photos across users
- **partner sharing** can expose one user's full timeline to another, like iCloud family features
- public share links (optionally with password/expiry) work for relatives without accounts

The phones keep using their native camera apps. The Immich app syncs the camera roll to the homelab in the background; photos are then viewable on every device through app or browser. External access for uploads on the go runs through [Cloudflare Tunnel](../../infrastructure/platform/ingress/cloudflare-tunnel).

---

## Used For

- automatic photo/video backup from iOS and Android
- family photo library with private per-user areas
- shared albums and partner sharing
- face recognition and semantic search, fully local
- replacing iCloud Photos / Google Photos storage plans

---

## Strengths

- Best-in-class mobile backup experience among self-hosted options.
- Local ML: face grouping and object search without cloud services.
- True multi-user design with private libraries, sharing and quotas.
- OIDC support for Keycloak SSO.
- Very active development and large community.

---

## Weaknesses

- Fast-moving project: breaking changes between releases happen; read release notes before upgrading.
- Multi-service architecture is heavier to operate than single-container apps.
- ML features want real CPU (or GPU) and RAM.
- Photo storage grows forever — capacity and backup planning is mandatory.
- Deleting the app from a phone does not delete photos there; the mental model (what lives where) must be explained to the family.

---

## Infrastructure Dependencies

| Dependency | Purpose |
|---|---|
| [`../../infrastructure/platform/databases/postgresql`](../../infrastructure/platform/databases/postgresql) | Metadata database (requires the pgvecto.rs/vector extension) |
| [`../../infrastructure/platform/databases/redis`](../../infrastructure/platform/databases/redis) | Job queue and caching |
| [`../../infrastructure/platform/storage/longhorn`](../../infrastructure/platform/storage/longhorn) | Photo/video storage volumes |
| [`../../infrastructure/platform/ingress/traefik`](../../infrastructure/platform/ingress/traefik) | HTTP(S) ingress |
| [`../../infrastructure/platform/ingress/cert-manager`](../../infrastructure/platform/ingress/cert-manager) | TLS certificates |
| [`../../infrastructure/platform/ingress/cloudflare-tunnel`](../../infrastructure/platform/ingress/cloudflare-tunnel) | Mobile upload from outside the LAN |
| [`../../infrastructure/platform/security/rights-management/keycloak`](../../infrastructure/platform/security/rights-management/keycloak) | Family SSO via OIDC |
| [`../../infrastructure/platform/backup/velero`](../../infrastructure/platform/backup/velero) | Backups — irreplaceable data lives here |

---

## Application Examples

- Every family phone backs up its camera roll automatically over night.
- A shared "Vacation 2026" album collects photos from all four family members.
- Search "beach" or a person's face and find photos instantly, all locally.
- Grandparents receive a public link to the newest album, no account needed.
- Cancel the iCloud storage plan once a restore test has proven the backups.

---

## Comparison Notes

| System | Best at | Tradeoff |
|---|---|---|
| Immich | Google-Photos-class experience, self-hosted | Fast-moving, heavier stack |
| Nextcloud Photos/Memories | Photos inside the existing Nextcloud | Weaker mobile backup and search |
| PhotoPrism | Powerful indexing and search of existing folders | Multi-user and mobile backup are weaker |
| LibrePhotos | Open source ML photo management | Smaller community, rougher edges |

---

## Hands-On Start

Deployment files should eventually live under `helm-charts`.

First evaluation checklist:

1. Deploy PostgreSQL (with vector extension) and Redis first.
2. Deploy Immich server + machine learning with dedicated storage volumes.
3. Create one test user, install the mobile app, verify background backup on the LAN.
4. Add Keycloak OIDC login and one account per family member.
5. Test shared albums and partner sharing between two users.
6. Enable remote upload through Cloudflare Tunnel.
7. Back up database and originals with Velero and **test a restore** before deleting anything from iCloud.

---

## Runtime Status

Immich is currently `⚫ Inactive`. It is planned as the family photo platform once storage, backup and identity are production-ready — photos are the least replaceable data in the homelab, so backups come first.

---

## Future Deployment Link

Planned deployment location:

```text
../../helm-charts/applications/immich/
```

---

## Documentation

- [Immich documentation](https://immich.app/docs/overview/introduction)
- [Immich GitHub](https://github.com/immich-app/immich)
- [Immich OAuth/OIDC setup](https://immich.app/docs/administration/oauth)
- [Wikipedia: Google Photos](https://en.wikipedia.org/wiki/Google_Photos) (the product being replaced)
