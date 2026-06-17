# Infrastructure

[<- Back to Repository Overview](../README.md)

This directory describes the homelab infrastructure layer: network configuration, bare-metal provisioning, Kubernetes platform components, shared services and cluster-hosted applications.

It is intentionally documentation-first. Actual deployment assets such as Helm charts, HelmRelease files, values files, Kustomize overlays or Argo CD applications should live under [`../helm-charts`](../helm-charts) as that directory is populated. Infrastructure documentation links to those deployment assets instead of duplicating them.

---

## Why This Matters

Infrastructure is the foundation that applications rely on. It includes the physical network, node provisioning, Kubernetes platform services, storage, databases, messaging, observability, security and deployment workflows.

In a homelab, infrastructure documentation is especially valuable because the same person is usually the hardware owner, network admin, platform engineer and application developer. Writing decisions down avoids rebuilding the same understanding every time something breaks.

In companies, this layer is often owned by platform, infrastructure or SRE teams. The goals are similar: repeatability, operational clarity, recoverability, security and a clear boundary between platform services and application code.

---

## What You Can Do With It

- document network and hardware decisions
- define repeatable provisioning workflows
- describe shared Kubernetes platform services
- explain why tools were chosen
- keep deployment assets linked but separate
- create a decision log for future rebuilds
- make the homelab understandable to other developers

---

## Directory Layout

```text
infrastructure/
├── network/
│   └── mikrotik/
├── provisioning/
│   └── ansible/
└── kubernetes/
    ├── api/
    │   └── graphql/
    ├── applications/
    │   ├── nextcloud/
    │   └── plex/
    ├── backup/
    │   └── velero/
    ├── bootstrap/
    ├── databases/
    │   ├── influxdb/
    │   ├── mongodb/
    │   ├── mysql/
    │   ├── postgresql/
    │   └── redis/
    ├── gitops/
    │   ├── argocd/
    │   └── flux/
    ├── messaging/
    │   ├── kafka/
    │   ├── nats/
    │   └── rabbitmq/
    ├── networking/
    │   ├── cert-manager/
    │   ├── cilium/
    │   ├── ingress/
    │   ├── metallb/
    │   └── traefik/
    ├── observability/
    │   ├── logging/
    │   │   ├── fluent-bit/
    │   │   └── opensearch/
    │   ├── metrics/
    │   │   ├── grafana/
    │   │   └── prometheus/
    │   └── tracing/
    │       ├── jaeger/
    │       ├── opentelemetry-collector/
    │       └── zipkin/
    ├── operators/
    ├── registry/
    │   ├── artifact-repository/
    │   └── harbor/
    ├── runtime/
    │   ├── dapr/
    │   └── service-mesh/
    ├── security/
    │   ├── external-secrets/
    │   ├── rights-management/
    │   │   └── keycloak/
    │   ├── sealed-secrets/
    │   └── secret-store/
    └── storage/
        ├── longhorn/
        └── minio/
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
| [`./network`](./network) | Physical and logical network configuration, especially MikroTik and VLAN planning |
| [`./provisioning`](./provisioning) | Repeatable node setup, mainly Ansible and bootstrap workflows |
| [`./kubernetes`](./kubernetes) | Cluster components, platform services, databases, messaging, observability, user-facing applications and operators |

---

## Documentation Rule

Every component gets a local `README.md` next to its future configuration.

Example:

```text
infrastructure/kubernetes/messaging/nats/README.md
```

That file explains what NATS is, why it exists in this project, when it should run, what alternatives exist and where the future Helm deployment will live.
