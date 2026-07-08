# Service Mesh

[<- Back to Runtime Platform](../README.md)

A service mesh manages service-to-service traffic, usually through sidecars or node-level proxies.

Typical features include mTLS, retries, traffic splitting, observability and policy enforcement.

A service mesh adds a traffic-management layer between services. Instead of every application implementing mutual TLS, retries, timeouts and traffic policy itself, a proxy can handle much of that behavior.

In many service meshes, each workload gets a sidecar proxy. Application traffic passes through the proxy, and the mesh control plane configures those proxies. Some newer approaches use node-level or eBPF-based proxies instead of one sidecar per pod.

For beginners, the important point is that a service mesh is mostly about service-to-service network traffic. It is not the same as Dapr, which exposes application building-block APIs.

---

## Recommendation

Do not start with a service mesh. First build normal Kubernetes networking, ingress, metrics and a few real services. Add a mesh only when there is a clear reason.

If a mesh is needed later, evaluate Linkerd first because it is easier to operate than Istio. Evaluate Istio when advanced traffic management, Gateway API integration or complex policy is a real requirement.

---

## What It Can Be Used For

- mutual TLS between internal services
- traffic splitting between service versions
- retries, timeouts and circuit-breaking policies
- service-to-service observability
- policy enforcement for east-west traffic
- learning zero-trust networking patterns

---

## Strengths

- Standardizes service-to-service security and traffic behavior.
- Can add mTLS without every app implementing TLS directly.
- Useful for controlled rollouts and traffic splitting.
- Provides visibility into service communication.
- Teaches production patterns used in large Kubernetes environments.

---

## Weaknesses

- Adds meaningful operational complexity.
- Can make networking harder to debug for beginners.
- Sidecar-based meshes add resource overhead.
- Many homelab services do not need mesh features early.
- Misconfigured policy can break service communication.

---

## Candidates

| Candidate | Location | Homelab fit | Business fit | Notes |
|---|---|---|---|---|
| Linkerd | Self-hosted | Recommended first mesh | Good | Lightweight, beginner-friendly mesh with mTLS focus |
| Istio | Self-hosted | Advanced | Strong standard | Very powerful, heavier and more complex |
| Cilium service mesh | Self-hosted | Research | Good if Cilium-first | Interesting if Cilium is already the networking foundation |
| Dapr | Self-hosted | Separate runtime | Not a pure mesh | Provides application building blocks |

---

## Application Examples

- Enforce mTLS between internal services without each service implementing TLS itself.
- Split traffic between two versions of an API during a rollout.
- Add retries and timeouts consistently for service-to-service calls.
- Observe service communication paths without adding custom tracing code everywhere.
- Test production-style zero-trust networking patterns in the homelab.

---

## Comparison Notes

Linkerd is the best first mesh candidate when the goal is learning mTLS and simple traffic visibility. Istio is stronger for complex traffic management and policy, but it is heavier. Cilium service mesh is interesting because Cilium is already the recommended CNI. Dapr should stay separate in the documentation because it provides application APIs, not just network traffic management.

---

## Runtime Status

Service mesh is currently `⚫ Inactive` and research-only for now.

---

## Future Deployment Link

Planned deployment location:

```text
../../../../helm-charts/infrastructure/platform/runtime/service-mesh/
```

---

## Documentation

- [Linkerd documentation](https://linkerd.io/2/overview/)
- [Istio documentation](https://istio.io/latest/docs/)
- [Cilium service mesh documentation](https://docs.cilium.io/en/stable/network/servicemesh/)
- [Wikipedia: Service mesh](https://en.wikipedia.org/wiki/Service_mesh)
- [Wikipedia: Mutual authentication](https://en.wikipedia.org/wiki/Mutual_authentication)
