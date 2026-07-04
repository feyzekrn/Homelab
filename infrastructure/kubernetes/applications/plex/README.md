# Plex

[<- Back to User-Facing Applications](../README.md)

Plex is a self-hosted media server for organizing and streaming movies, shows, music and other media.

In this homelab, it belongs under `applications` because it is a user-facing workload. It is not required for Kubernetes itself, but it is a useful real-world app for testing storage, networking and hardware capabilities.

Plex scans a media library, organizes metadata and streams media to clients such as TVs, phones, browsers and media boxes. It is not a database, ingress controller or storage system; it is an application that uses those platform services.

Plex is interesting in Kubernetes because it has practical infrastructure needs: persistent metadata, access to large media files, stable network exposure and sometimes hardware transcoding. That makes it a good example of an application that may be possible in Kubernetes but still needs careful placement.

---

## Why It Fits

Plex is a good homelab workload because it stresses different parts of the platform than typical web apps:

- large media libraries
- persistent metadata
- ingress or LAN exposure
- storage layout
- optional hardware transcoding
- node placement decisions

It also forces a practical decision: some workloads are easier to run on Kubernetes than others. Plex can run in Kubernetes, but media paths, GPU/iGPU access and network discovery need careful handling.

---

## Used For

- media library management
- local streaming
- remote streaming experiments
- testing large persistent media volumes
- testing hardware transcoding support
- learning node affinity and workload placement

---

## Strengths

- Real workload with visible user value.
- Tests storage layout and LAN service exposure.
- Good case study for node affinity and hardware access.
- Mature client ecosystem.
- Useful comparison between Kubernetes and dedicated-host deployment.

---

## Weaknesses

- Hardware transcoding can complicate Kubernetes scheduling.
- Media files may be better stored outside Longhorn volumes.
- Network discovery and remote access can be more awkward than normal web apps.
- Some features depend on Plex account or paid plan.
- It is optional and should not block core platform work.

---

## Infrastructure Dependencies

| Dependency | Purpose |
|---|---|
| [`../../storage/longhorn`](../../storage/longhorn) | Metadata or configuration volume if suitable |
| External media storage | Large media files usually belong on dedicated storage |
| [`../../networking/traefik`](../../networking/traefik) | Optional HTTP(S) exposure |
| MetalLB / LAN networking | Stable LAN access to Plex |
| Node labels / affinity | Pin Plex to a node with media access or hardware transcoding |

---

## Application Examples

- Stream local media inside the LAN.
- Keep Plex metadata on persistent storage.
- Pin Plex to a specific node with media disks attached.
- Test Intel Quick Sync or other hardware transcoding later.
- Compare Kubernetes deployment against running Plex directly on a dedicated host.

---

## Comparison Notes

| System | Best at | Tradeoff |
|---|---|---|
| Plex | Polished media server ecosystem and clients | Some features depend on Plex account or paid plan |
| Jellyfin | Fully open-source media server | Less polished client ecosystem for some devices |
| Emby | Media server with commercial features | Licensing model differs |

---

## Kubernetes Notes

Plex is not a core platform service. Treat it as an application with special hardware and storage needs.

Before deploying:

- decide where media files live
- decide whether transcoding is needed
- decide whether the pod needs access to `/dev/dri`
- pin the workload to the right node
- document backup needs for metadata separately from media files

---

## Hands-On Start

Deployment files should eventually live under `helm-charts`.

First evaluation checklist:

1. Start without hardware transcoding.
2. Mount a small test media directory.
3. Expose Plex only on the LAN first.
4. Verify metadata persists after pod restart.
5. Add node affinity if the media path exists only on one node.
6. Evaluate hardware transcoding only after the basic deployment is stable.

---

## Runtime Status

Plex is currently `⚫ Inactive`. Add it only after the storage and networking model for user-facing apps is clear.

---

## Future Deployment Link

Planned deployment location:

```text
../../../../helm-charts/applications/plex/
```

---

## Documentation

- [Plex Support](https://support.plex.tv/)
- [Plex Docker image](https://hub.docker.com/r/plexinc/pms-docker)
- [Wikipedia: Plex](https://en.wikipedia.org/wiki/Plex_(software))
- [Wikipedia: Media server](https://en.wikipedia.org/wiki/Media_server)
