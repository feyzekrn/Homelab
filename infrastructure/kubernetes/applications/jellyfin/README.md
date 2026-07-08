# Jellyfin

[<- Back to User-Facing Applications](../README.md)

Jellyfin is a fully open-source, self-hosted media server for organizing and streaming movies, shows and music.

In this homelab, Jellyfin is the **chosen media server**. [Plex](../plex) remains documented for comparison, but the deployment plan is Jellyfin: it is completely free software, has no account requirement, no paywalled features and no phone-home dependency — which matches the self-hosting philosophy of this whole repository.

Jellyfin scans media libraries, fetches metadata and streams to clients on TVs, phones, browsers and media boxes. It is a community-driven fork of Emby and shares the same infrastructure profile as Plex: persistent metadata, large media volumes, LAN exposure and optional hardware transcoding.

---

## Why It Fits

Jellyfin fits this homelab for the same platform reasons as any media server, plus philosophical ones:

- large media libraries test storage layout decisions
- persistent metadata tests volume handling
- optional hardware transcoding tests device access (`/dev/dri`) and node placement
- no external account: the server works fully offline and stays under local control
- every feature is free — remote access, hardware transcoding, all clients

The decision against Plex is not about quality. Plex has the more polished ecosystem; Jellyfin has no strings attached. For a repository built around open, self-controlled infrastructure, Jellyfin is the consistent choice.

---

## Used For

- media library management
- local streaming to TVs, phones and browsers
- remote streaming through the chosen access path
- testing large persistent media volumes
- testing hardware transcoding (Intel Quick Sync)
- learning node affinity and workload placement

---

## Strengths

- 100% free and open source; no accounts, subscriptions or feature gates.
- Hardware transcoding without a paid pass.
- No external dependency: works fully offline.
- Active community and steady release cadence.
- Same learning value as Plex for storage and placement decisions.

---

## Weaknesses

- Client apps on some platforms are less polished than Plex's.
- Metadata matching sometimes needs more manual care.
- No managed relay for remote access — external exposure is your own responsibility (see [Cloudflare Tunnel](../../networking/cloudflare-tunnel)).
- Hardware transcoding still complicates Kubernetes scheduling, same as Plex.

---

## Infrastructure Dependencies

| Dependency | Purpose |
|---|---|
| [`../../storage/longhorn`](../../storage/longhorn) | Metadata and configuration volume |
| External media storage | Large media files usually belong on dedicated storage |
| [`../../networking/traefik`](../../networking/traefik) | HTTP(S) exposure |
| [`../../networking/metallb`](../../networking/metallb) | Stable LAN access |
| [`../../networking/cloudflare-tunnel`](../../networking/cloudflare-tunnel) | Optional remote access without port forwarding |
| Node labels / affinity | Pin Jellyfin to the node with media access or iGPU |
| [`../../security/rights-management/keycloak`](../../security/rights-management/keycloak) | Optional SSO via plugin (LDAP/OIDC) |

---

## Application Examples

- Stream the local media library inside the LAN.
- Keep Jellyfin metadata on a persistent Longhorn volume.
- Pin the workload to the node with the media disks and Intel iGPU.
- Enable Quick Sync transcoding by mounting `/dev/dri`.
- Create separate users for family members with their own watch state.

---

## Comparison Notes

| System | Best at | Tradeoff |
|---|---|---|
| Jellyfin | Fully open source, all features free | Some clients less polished |
| [Plex](../plex) | Polished ecosystem and client coverage | Account required, key features paywalled |
| Emby | Middle ground, commercial | Licensing model, closed components |

---

## Kubernetes Notes

Jellyfin inherits every operational consideration documented for [Plex](../plex#kubernetes-notes): media path placement, transcoding hardware, node affinity and separate backup treatment for metadata versus media files. Read that section too — the decisions are identical, only the software differs.

Before deploying:

- decide where media files live (usually not on Longhorn)
- decide whether the pod needs `/dev/dri` for Quick Sync
- pin the workload to the right node
- back up the config/metadata volume; media files follow their own backup strategy

---

## Hands-On Start

Deployment files should eventually live under `helm-charts`.

First evaluation checklist:

1. Start without hardware transcoding.
2. Mount a small test media directory.
3. Expose Jellyfin only on the LAN first.
4. Verify metadata and watch state persist after a pod restart.
5. Add node affinity for the media/iGPU node.
6. Evaluate Quick Sync transcoding once the basic deployment is stable.
7. Consider remote access via Cloudflare Tunnel last.

---

## Runtime Status

Jellyfin is currently `⚫ Inactive`. It is the planned media server for this homelab and will be added once the storage and networking model for user-facing apps is in place.

---

## Future Deployment Link

Planned deployment location:

```text
../../../../helm-charts/applications/jellyfin/
```

---

## Documentation

- [Jellyfin documentation](https://jellyfin.org/docs/)
- [Jellyfin GitHub](https://github.com/jellyfin/jellyfin)
- [Wikipedia: Jellyfin](https://en.wikipedia.org/wiki/Jellyfin)
- [Wikipedia: Media server](https://en.wikipedia.org/wiki/Media_server)
