# Backup

[<- Back to Kubernetes](../README.md)

Backups are not optional once the cluster stores useful data.

This directory documents backup tooling, restore tests and disaster recovery decisions.

---

## Components

| Component | Role | Documentation |
|---|---|---|
| Velero | Kubernetes resource and volume backup orchestration | [velero](./velero) |

---

## Rule

A backup that has never been restored is only a hope. Every important backup workflow should have a documented restore test.
