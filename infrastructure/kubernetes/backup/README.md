# Backup

[<- Back to Kubernetes](../README.md)

Backups are not optional once the cluster stores useful data.

This directory documents backup tooling, restore tests and disaster recovery decisions.

---

## Why This Matters

A backup strategy is only real if restore has been tested. Kubernetes resources, persistent volumes, database dumps and object storage may all need different recovery workflows.

In a homelab, backup work teaches what data is actually important and how painful a rebuild would be. In companies, backup and disaster recovery are tied to recovery-time objectives, recovery-point objectives, compliance and business continuity.

---

## What You Can Do With It

- back up Kubernetes resources
- back up persistent volumes
- test namespace restore
- practice disaster recovery after a cluster rebuild
- separate GitOps-restored manifests from runtime data
- document which systems need database-native backups

---

## Components

| Path | Role |
|---|---|
| [`./velero`](./velero) | Kubernetes resource and volume backup orchestration |

---

## Rule

A backup that has never been restored is only a hope. Every important backup workflow should have a documented restore test.
