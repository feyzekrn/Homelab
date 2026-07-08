# Nextcloud Synchronization Guide

[<- Back to Nextcloud](./README.md)

This guide explains how Nextcloud replaces iCloud and OneDrive as the **single source of truth** for files, calendars and contacts — while Apple and Windows devices keep using their native apps.

The key idea: the devices do not get a second, parallel data store. Apple Calendar, Apple Contacts, Finder, Windows Explorer and Outlook all speak open protocols that Nextcloud implements. The apps stay; only the account behind them changes from Apple/Microsoft to the homelab.

| Data | Protocol | What it means |
|---|---|---|
| Files | WebDAV + sync client | Folder sync or direct network drive |
| Calendars | CalDAV | Standard calendar sync protocol |
| Contacts | CardDAV | Standard contact sync protocol |
| Photos | (see [Immich](../immich)) | Photos are handled by Immich, not Nextcloud |

Every entry created on any device syncs to Nextcloud, and from there to every other device. Nothing is stored "in iCloud *and* in Nextcloud" — Nextcloud **is** the store; the devices hold caches and offline copies.

---

## Source Of Truth Model

```text
                    ┌──────────────────────────┐
                    │        Nextcloud         │
                    │  files · calendar · contacts
                    └──────┬──────┬──────┬─────┘
             CalDAV/CardDAV│      │WebDAV│
            ┌──────────────┘      │      └──────────────┐
     ┌──────┴──────┐      ┌───────┴──────┐      ┌───────┴──────┐
     │ iPhone/iPad │      │    macOS     │      │   Windows    │
     │ native apps │      │ native apps  │      │ Explorer/    │
     │             │      │ + sync client│      │ Outlook/etc. │
     └─────────────┘      └──────────────┘      └──────────────┘
```

Prerequisite for all of this: the Nextcloud hostname must be reachable from everywhere the devices go, with valid TLS. Inside the LAN that is Traefik + cert-manager; outside it is [Cloudflare Tunnel](../../infrastructure/platform/ingress/cloudflare-tunnel). Sync protocols retry silently, but an unreachable server means stale data until the device is home again.

---

## Calendar Sync (CalDAV)

Nextcloud's Calendar app provides CalDAV at:

```text
https://cloud.example.com/remote.php/dav
```

### iPhone / iPad / macOS

Apple's Calendar has first-class CalDAV support:

1. Settings → Calendar → Accounts → Add Account → **Other** → **Add CalDAV Account** (macOS: System Settings → Internet Accounts → Add Other Account).
2. Server: `cloud.example.com`, plus Nextcloud username and an **app password** (see below).
3. Enable Calendars (and Reminders — Nextcloud Tasks appears as Reminders lists).
4. In Calendar, set the default calendar to a Nextcloud calendar so new events go to the homelab by default.

A new appointment created in Apple Calendar is written directly to Nextcloud via CalDAV. iCloud is not involved. Once all calendars are migrated (export `.ics` from iCloud, import in Nextcloud), disable Calendar under the iCloud account.

### Windows

- **Thunderbird** supports CalDAV natively and is the most reliable free option.
- **Outlook** has no native CalDAV; use a connector like Caldav Synchronizer (open source).
- The Nextcloud web calendar is always available as fallback.

---

## Contact Sync (CardDAV)

Same pattern, same DAV endpoint, via the Nextcloud Contacts app.

### iPhone / iPad / macOS

1. Settings → Contacts → Accounts → Add Account → Other → **Add CardDAV Account**.
2. Server `cloud.example.com`, username, app password.
3. Set Default Account for new contacts to the CardDAV account.

New contacts saved on the phone land in Nextcloud and appear on every other device. After migrating existing contacts (export vCard from iCloud, import in Nextcloud), disable Contacts under iCloud.

### Windows

Thunderbird handles CardDAV natively; Caldav Synchronizer covers Outlook contacts as well.

---

## File Sync (WebDAV And Sync Clients)

Files support two complementary modes:

### Sync client (recommended for laptops)

The Nextcloud desktop client (macOS, Windows, Linux) syncs chosen folders bidirectionally and supports **virtual files**: everything is visible in Finder/Explorer, but content downloads on demand — the same experience as OneDrive's Files-On-Demand or iCloud's "Optimize Mac Storage". The synced folder appears in the Finder sidebar and Explorer like any cloud drive.

### Direct WebDAV mount (no local copy)

For accessing files without syncing them:

- **Finder (macOS)**: Go → Connect to Server → `https://cloud.example.com/remote.php/dav/files/USERNAME/`
- **Explorer (Windows)**: Map Network Drive → same URL
- **iOS Files app**: the Nextcloud iOS app registers as a Files provider, so Nextcloud appears inside the native Files app next to iCloud Drive

WebDAV mounts read and write directly against the server — nothing is stored locally, which is ideal for occasionally-used archives. For daily-driver folders (Documents, Desktop) the sync client is more robust, because native OS WebDAV clients are slow and dislike flaky connections.

### iPhone

The Nextcloud iOS app provides browsing, offline favorites, automatic upload and Files-app integration. (Camera photos belong in [Immich](../immich) instead — better mobile backup and timeline.)

---

## App Passwords, Not The Real Password

Devices should never store the main account password. Nextcloud issues per-device app passwords under Settings → Security → "Create new app password" — one per device ("iPhone Feyzullah", "Windows Desktop", …).

Benefits:

- a lost device is revoked individually, nothing else re-authenticates
- required anyway once Keycloak SSO is enabled, since DAV clients cannot do browser login flows
- the security page shows which device connected when

With [Keycloak SSO](./multi-user-family.md) enabled, browser login goes through Keycloak while DAV clients keep using app passwords — this split is normal and by design.

---

## Migration Checklist (iCloud/OneDrive → Nextcloud)

1. Deploy Nextcloud with valid TLS and external reachability.
2. Create the personal account (via Keycloak once available).
3. Export calendars from iCloud (`.ics`) → import into Nextcloud Calendar.
4. Export contacts from iCloud (vCard) → import into Nextcloud Contacts.
5. Add CalDAV + CardDAV accounts on every Apple device; set them as default for new items.
6. Verify two-way sync: create an event on the phone, see it in the web UI, and vice versa.
7. Install desktop sync clients; move working folders into the synced area.
8. Copy remaining iCloud Drive/OneDrive files over.
9. Run both systems in parallel for a few weeks.
10. Disable Calendar/Contacts/Drive under the iCloud account — **only after backups are proven** ([Velero](../../infrastructure/platform/backup/velero) restore test).

---

## Sync Traps Worth Knowing

- **Default account settings matter.** If iOS still defaults new events/contacts to iCloud, data silently splits across both worlds. Set defaults immediately after adding the accounts.
- **Never sync the same folder with two tools** (e.g. OneDrive and Nextcloud client) — guaranteed conflict duplicates.
- **Reminders/Tasks**: Nextcloud Tasks syncs through the same CalDAV account and appears in Apple Reminders.
- **Background jobs**: configure Nextcloud cron properly, otherwise sync and notifications degrade.
- **The server is now your responsibility.** iCloud's redundancy must be replaced by real backups. No restore test, no iCloud cancellation.

---

## Documentation

- [Nextcloud desktop client docs](https://docs.nextcloud.com/desktop/latest/)
- [Nextcloud iOS/Android app docs](https://docs.nextcloud.com/#clients)
- [Nextcloud DAV endpoints reference](https://docs.nextcloud.com/server/latest/user_manual/en/groupware/sync_ios.html)
- [Wikipedia: CalDAV](https://en.wikipedia.org/wiki/CalDAV)
- [Wikipedia: CardDAV](https://en.wikipedia.org/wiki/CardDAV)
- [Wikipedia: WebDAV](https://en.wikipedia.org/wiki/WebDAV)
