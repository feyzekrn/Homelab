# Infrastructure

[<- Back to Repository Overview](../README.md)

This directory describes everything below the application layer: network configuration, bare-metal provisioning, Kubernetes platform components, shared databases, messaging, observability and runtime building blocks.

It is intentionally documentation-first. Actual deployment assets such as Helm charts, HelmRelease files, values files, Kustomize overlays or Argo CD applications should live under [`../helm-charts`](../helm-charts) once that directory exists. Infrastructure documentation links to those deployment assets instead of duplicating them.

---

## Directory Layout

```text
infrastructure/
├── network/
├── provisioning/
└── kubernetes/
    ├── bootstrap/
    ├── networking/
    ├── storage/
    ├── databases/
    ├── messaging/
    ├── api/
    ├── observability/
    ├── runtime/
    └── operators/
```

---

## What Belongs Here

Use this directory for shared infrastructure decisions:

- why a component exists in the homelab
- what problem it solves
- what alternatives were considered
- whether it should run permanently or only when needed
- operational notes, risks and upgrade considerations
- links to deployment assets in `helm-charts`

Do not put application source code here. Application and service code belongs under `services`, `apps` or a dedicated external repository.

---

## Main Areas

| Path | Purpose |
|---|---|
| [`network`](./network) | Physical and logical network configuration, especially MikroTik and VLAN planning |
| [`provisioning`](./provisioning) | Repeatable node setup, mainly Ansible and bootstrap workflows |
| [`kubernetes`](./kubernetes) | Cluster components, platform services, databases, messaging, observability and operators |

---

## Documentation Rule

Every component gets a local `README.md` next to its future configuration.

Example:

```text
infrastructure/kubernetes/messaging/nats/README.md
```

That file explains what NATS is, why it exists in this project, when it should run, what alternatives exist and where the future Helm deployment will live.
