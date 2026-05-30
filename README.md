# Autonomous Bare-Metal Kubernetes Homelab Cluster 🚀
### A Cloud-Native, DevOps, and Full-Stack Engineering Learning Journey

Welcome to my bare-metal Kubernetes (K8s) homelab cluster repository. This project is a curated, open-source showcase designed to demonstrate how a fleet of budget-friendly **Lenovo ThinkCentre M910q Tiny** PCs can be transformed into an enterprise-grade mini data center. This repo is not a manual how to setup your future cluster. It will show you my ups and downs, the debates and questions i had in my head and how i solved or decided. starting in the setup of the hardware, and never finding an end in the software. I am planing to start small and always make upgrades as needed in both hardware and software. Maybe someone will check this out and locate improvements i wasn't able to see myself.

This repository serves two purposes:
1. **My Personal Skill Accelerator:** Mastering advanced Kubernetes, Networking Skills, Cloud-Native Engineering, Go (Golang), Python automation, DevOps, and modern Full-Stack UI design (Next.js / Flutter).
2. **A Blueprint for Developers:** Providing a practical guide and inspiration on how to build a highly professional, automated, and self-hosted infrastructure on a strict budget.


### My person
I am not new into this business, I already work as Full-Stack Engineer & Architect since 6 years in a corporate business. I already have senior skills in coding with all kind of language especially in JS, TS, C#, Java, managed Kubernetes in AWS EKS which i am working with daily. During my professional work I am suiting a role as technical lead in many different Projects. This project will help me to get back more into doing myself and learning newer version of the techstack i used previously or learn new stuff just like Golang or Flutter instead of evaluating stuff and writing tickets for coworkers. Next to my profession as Software Engineer and fulltime Business Informatics Studies this project will be my escape from reality

---

## 🎯 The Core Learning Pillars (My Tech Stack Goals)

This homelab is structurally engineered to master specific, high-demand industry skills:

### 1. ☸️ Advanced Kubernetes & Cloud-Native Engineering
* **Deep K8s Internals:** Going far beyond basic deployments. This involves tweaking container runtimes, advanced scheduling, custom resource definitions (CRDs), and debugging multi-node failures.
* **Storage & Data Integrity:** Implementing **Longhorn** distributed block storage across asymmetric hardware.
* **The DB & Messaging Matrix:** Hosting and optimizing production-grade instances of `PostgreSQL`, `MySQL`, `MongoDB`, `Redis`, and `RabbitMQ`.
* **Telemetry & Big Data:** Aggregating infrastructure and application metrics using an active `ELK Stack` (Elasticsearch, Logstash, Kibana).

### 2. 🐹 Go (Golang) Core Mastery
* **Kubernetes Operators:** Writing custom K8s operators in Go to automate the lifecycle of my application stack.
* **High-Performance Microservices:** Building cloud-native backends utilizing Go's brutal speed and native concurrency (goroutines).

### 3. 🐍 Python Home Automation
* **Hardware & IoT Control:** Scripting automated triggers based on server metrics (e.g., node temperatures, power usage, physical intrusion alerts).
* **Intel vPro/AMT API Integration:** Writing Python wrappers to interact with Intel's hardware management layer to automatically boot, reboot, or isolate physical nodes based on cluster health.

### 4. 🎨 Next.js & Flutter UI/UX Engineering
* **Next.js Web Admin Dashboards:** Building visually stunning, responsive server management panels with server-side rendering (SSR), real-time WebSockets, and tailwind-crafted analytics.
* **Flutter Mobile Interfaces:** Developing cross-platform mobile apps to monitor cluster status, receive critical push notifications, and trigger vPro hardware actions right from my phone.

### 5. 🌐 Infrastructure as Code (IaC) & Advanced Networking
* **Network Engineering:** Deploying a secure **Multi-Homing** network. A budget unmanaged switch isolates Intel vPro (1G), while a **MikroTik CRS310-8G+2S+IN** leverages **L3 Hardware Offloading** to route heavy Kubernetes & Storage traffic at native **2.5 Gbps**, entirely offloading our internet router.
* **GitOps & DevOps Pipelines:** Managing the entire infrastructure programmatically using `Terraform` (for MikroTik configuration), `Ansible` (for bare-metal provisioning), and GitOps (for continuous application deployment).

---

## 🏗️ Hardware Architecture (Budget-Optimized)
Check out more detials: 

| Component | Specification (Per Node) | Strategy / Notes |
| :--- | :--- | :--- |
| **Compute** | Lenovo ThinkCentre M910q Tiny | Highly efficient, cheap, vPro/AMT capable. |
| **CPU Path** | Intel i5-6500T (Initial) -> i7-7700T | Step-by-step upgrade to prevent bottlenecks. |
| **RAM Path** | Symmetrical: 16GB, 8GB, 8GB -> 32GB each | Cost-efficient start for local hobby projects. |
| **Storage** | 258GB Samsung 850 PRO 2,5 SSD | The sweet spot to handle heavy DB writes & Cluster logs for home-applications. |

### 🔌 Physical Topology

* **Lenovo Tiny Nodes** (Dual Cable Setup):
  * Onboard Port (1G) -> Connected to **Netgear GS308 Switch** (Dedicated vPro & K8s Management Network)
  * M.2 Expansion Port (2.5G) -> Connected to **MikroTik CRS310 Switch** (Dedicated K8s Data & Storage Network)
* **Switch Interconnection**:
  * Netgear GS308 (1G) -> Uplinked directly to **MikroTik CRS310** (VLAN 10 Trunking)
  * MikroTik CRS310 (2.5G Core) -> Uplinked to **Old Internet Router** (Strictly for external WAN internet access only)

---

## 🗂️ Repository Structure

* `/talus` - OS running on the machines.
* `/setup` - Introduction to hardware setup and evaluation why I decided to use which component
* `/terraform` - Network infrastructure as code (VLAN configs, L3 interfaces on the MikroTik Switch).
* `/k8s-infra` - Core cluster components (Cilium/Calico CNI, Longhorn Storage, MetalLB).
* `db-designs` - The Design Patterns ORM sheets and ER Diagrams of the publicly availably DBs
* `/k8s-apps` - GitOps declarations for the database stack, Redis caches, and ELK logging.
* `/services-go` - Source code for custom cloud-native Go microservices and K8s operators.
* `/automation-py` - Hardware automation, vPro controllers, and smart-home IoT integrations.
* `/dashboard_next.js` - Source code for the web-based administrative command center.
* `/mobile-flutter` - Cross-platform companion app for real-time cluster monitoring.

---

## 🛠️ The Clean Rack Integration

To ensure the homelab looks as professional as it operates, the physical layout features:
* **3D-Printed 1U Mounts:** Fitting three Lenovo Tinys side-by-side with custom front-facing **Keystone slots**.
* **Matte-Black 1U Patchpanel:** Using 0.25m slim patch cables to cleanly route the dual-network lines (vPro and 2.5G) directly to the switches without visible clutter.
