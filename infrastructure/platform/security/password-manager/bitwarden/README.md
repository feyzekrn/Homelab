# Bitwarden (Vaultwarden)

[<- Back to Password Manager](../README.md)

Bitwarden is an open-source password manager with clients for every platform. Vaultwarden is a lightweight, unofficial server implementation of the Bitwarden API — and the standard way to self-host it in a homelab.

The naming is worth untangling once:

- **Bitwarden** is the product and ecosystem: browser extensions, mobile apps, desktop apps, CLI. These official clients are what everyone actually uses day to day.
- **Bitwarden server (official)** is a heavy multi-container stack (or a newer unified image) designed for enterprises; some features sit behind paid licensing.
- **Vaultwarden** is a from-scratch Rust server speaking the same API. It runs in a single small container, uses SQLite or PostgreSQL, and unlocks most premium features (TOTP, emergency access, organizations) for free.

In this homelab, the plan is **Vaultwarden as the server with official Bitwarden clients** — the standard homelab combination. All vault data is encrypted end-to-end on the clients; the server stores only ciphertext.

---

## Why It Fits

Bitwarden was chosen because it is the most developer-friendly of the serious password managers:

- first-class **CLI** (`bw`) for scripting, dotfiles and CI use
- a real API and SDKs; secrets can be pulled programmatically
- SSH agent support in the desktop app for SSH key management
- open clients, open protocol, audited cryptography
- clients on literally everything: iOS, Android, macOS, Windows, Linux, every browser
- organizations/collections make family sharing clean

It also completes the security story of this repository: [Keycloak](../../rights-management/keycloak) answers "who are you" for homelab apps, the [Secret Store](../../secret-store) feeds applications, and Bitwarden holds the humans' credentials — including, carefully, the break-glass credentials for the homelab itself.

---

## Used For

- personal passwords, passkeys and TOTP codes for all family members
- shared family collections: WiFi, router, streaming, insurance logins
- developer workflows: `bw` CLI in scripts, SSH keys via desktop agent
- secure notes: recovery codes, license keys, document scans
- generating unique passwords everywhere, killing password reuse

---

## Strengths

- End-to-end encrypted: the server never sees plaintext, self-hosting risk is low.
- Vaultwarden is tiny — a fraction of the resources of the official stack.
- Official clients are polished and maintained by Bitwarden itself.
- Free access to features that are premium on bitwarden.com.
- Organizations model fits family sharing well.

---

## Weaknesses

- Vaultwarden is unofficial: client updates can occasionally outpace it; watch releases before upgrading.
- Availability matters: if the server is down *and* a client's local cache is gone, logins are blocked.
- Backup discipline is existential — an encrypted vault without backups is a total loss.
- Push notifications for instant sync need extra configuration (relay to Bitwarden's infrastructure).
- The admin panel must be protected and never exposed publicly.

---

## Critical Bootstrap Warning

The password manager is part of the homelab's own recovery path. If the credentials needed to fix the cluster are *only* inside a vault running *on* the cluster, a dead cluster locks you out of repairing it.

Rules:

- keep an offline export (encrypted) of break-glass credentials outside the cluster
- clients keep a local cache, so a short server outage is survivable — but do not rely on it
- test vault restore before the family moves in

---

## Infrastructure Dependencies

| Dependency | Purpose |
|---|---|
| [`../../../storage/longhorn`](../../../storage/longhorn) | Persistent volume for the vault database |
| [`../../../databases/postgresql`](../../../databases/postgresql) | Optional; SQLite is fine at family scale |
| [`../../../ingress/traefik`](../../../ingress/traefik) | HTTPS ingress — clients require valid TLS |
| [`../../../ingress/cert-manager`](../../../ingress/cert-manager) | TLS certificates |
| [`../../../ingress/cloudflare-tunnel`](../../../ingress/cloudflare-tunnel) | Sync away from home without port forwarding |
| [`../../../backup/velero`](../../../backup/velero) | Backups of the most critical small dataset in the lab |

---

## Application Examples

- Family members autofill logins on their phones from the homelab vault.
- A shared "Family" organization holds the WiFi password and streaming logins.
- `bw get password prod-db` inside a maintenance script instead of a plaintext env file.
- SSH keys served by the Bitwarden desktop agent instead of loose `~/.ssh` files.
- Emergency access lets a partner reach the vault if the owner is unavailable.

---

## Comparison Notes

| System | Best at | Tradeoff |
|---|---|---|
| Bitwarden + Vaultwarden | Full ecosystem, dev-friendly, light server | Unofficial server needs upgrade care |
| Bitwarden official server | Vendor-supported deployment | Heavy; features behind licensing |
| KeePassXC (+ file sync) | Fully offline, no server at all | No real multi-user, sync is DIY |
| 1Password | Most polished UX | Closed source, subscription, no self-hosting |
| Psono / Passbolt | Team-oriented self-hosting | Smaller ecosystems, weaker personal clients |

---

## Hands-On Start

Deployment files should eventually live under `helm-charts`.

First evaluation checklist:

1. Deploy Vaultwarden with a persistent volume and HTTPS through Traefik (clients refuse plain HTTP).
2. Disable open registration after creating the first accounts; secure the admin token via the secret workflow.
3. Install browser extension and mobile app against the self-hosted URL.
4. Import existing passwords (browser/1Password/KeePass exports).
5. Set up the family organization and one shared collection.
6. Configure backups and **run a restore drill** — before real passwords move in.
7. Add Cloudflare Tunnel access for syncing away from home.

---

## Runtime Status

Bitwarden/Vaultwarden is currently `⚫ Inactive`. It is a strong early candidate once ingress, TLS, storage and backups work — small footprint, huge daily value.

---

## Future Deployment Link

Planned deployment location:

```text
../../../../../helm-charts/infrastructure/platform/security/password-manager/bitwarden/
```

---

## Documentation

- [Bitwarden help center](https://bitwarden.com/help/)
- [Vaultwarden GitHub + wiki](https://github.com/dani-garcia/vaultwarden)
- [Bitwarden CLI documentation](https://bitwarden.com/help/cli/)
- [Wikipedia: Bitwarden](https://en.wikipedia.org/wiki/Bitwarden)
