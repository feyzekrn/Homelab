# Service Mesh

[<- Back to Runtime Platform](../README.md)

A service mesh manages service-to-service traffic, usually through sidecars or node-level proxies.

Typical features include mTLS, retries, traffic splitting, observability and policy enforcement.

---

## Recommendation

Do not start with a service mesh. First build normal Kubernetes networking, ingress, metrics and a few real services. Add a mesh only when there is a clear reason.

If a mesh is needed later, evaluate Linkerd first because it is easier to operate than Istio. Evaluate Istio when advanced traffic management, Gateway API integration or complex policy is a real requirement.

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
../../../../helm-charts/runtime/service-mesh/
```

---

## Documentation

- [Linkerd documentation](https://linkerd.io/2/overview/)
- [Istio documentation](https://istio.io/latest/docs/)
- [Cilium service mesh documentation](https://docs.cilium.io/en/stable/network/servicemesh/)
