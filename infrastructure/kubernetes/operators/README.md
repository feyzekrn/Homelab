# Kubernetes Operators

[<- Back to Kubernetes](../README.md)

Operators extend Kubernetes with application-specific automation. They usually manage lifecycle tasks that would otherwise become scripts or manual runbooks.

This directory tracks free operators that may be useful and future custom operators built for this homelab.

---

## Why This Matters

Some systems are too stateful or complex to manage well with a plain Deployment. Databases, message brokers, certificate systems and storage platforms often need backups, upgrades, failover, users, cluster membership and health checks. Operators encode that operational logic into Kubernetes controllers.

In a homelab, operators are useful because they teach how production-style Kubernetes platforms manage complex software. In companies, operators often become the standard way to run databases, messaging systems and platform components safely.

---

## What You Can Do With It

- run PostgreSQL with automated failover and backups
- manage RabbitMQ or Kafka clusters
- automate certificate lifecycle
- create custom controllers for hardware automation
- define custom resources for homelab operations
- learn Kubernetes reconciliation patterns

---

## Why Operators Matter

Stateful systems are more than a Deployment and a PVC. Databases, message brokers and storage systems need backups, failover, upgrades, user management and health checks. Operators encode that operational knowledge into Kubernetes controllers.

---

## Free Operators To Evaluate

| Operator | Component | Why it matters | Status |
|---|---|---|---|
| CloudNativePG | PostgreSQL | PostgreSQL clusters, backups and failover | Candidate |
| Percona Operator for MySQL | MySQL | MySQL lifecycle and backups | Candidate |
| Oracle MySQL Operator | MySQL | Official MySQL operator option | Candidate |
| MongoDB Community Kubernetes Operator | MongoDB | Replica set automation | Candidate |
| Redis Operator | Redis | Redis lifecycle and clustering experiments | Research |
| RabbitMQ Cluster Operator | RabbitMQ | RabbitMQ cluster lifecycle | Candidate |
| Strimzi | Kafka | Kafka operator if Kafka is evaluated later | Research |
| Prometheus Operator | Prometheus | Standard Kubernetes metrics stack management | Candidate |
| Grafana Operator | Grafana | Dashboard and datasource automation | Research |
| OpenTelemetry Operator | OpenTelemetry | Collector and auto-instrumentation management | Research |
| cert-manager | Certificates | Certificate lifecycle automation | Core |
| Longhorn Manager | Longhorn | Storage lifecycle managed by Longhorn | Core |

---

## Custom Operators

Future custom operators should live here conceptually and in `services` or a dedicated repository for source code.

Potential custom operators:

- node power state operator using Intel vPro
- cluster maintenance window operator
- hardware inventory operator
- temperature-aware workload policy operator
- homelab backup orchestration operator

Each custom operator should document:

- watched resources
- reconciled resources
- failure behavior
- permissions required
- CRD examples
- deployment link

---

## Deployment Rule

Operator documentation lives here. Operator Helm charts, values and installation files should be linked from:

```text
../../../helm-charts/operators/<operator-name>/
```
