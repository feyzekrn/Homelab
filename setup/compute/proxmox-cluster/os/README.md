# Operating System — Proxmox VE

[← Back to proxmox-cluster](../README.md)

The MS-01 runs **Proxmox VE** — a bare-metal hypervisor based on Debian. Unlike the Kubernetes nodes, there is no phased OS strategy here: Proxmox is both the learning environment and the end state for this machine.

---

## Why Proxmox VE?

- **It is the point of the machine.** The MS-01 exists to host VMs and LXC containers — OPNsense, the NAS, the family apps. Proxmox is the open-source standard for exactly this job: KVM virtualization plus lightweight LXC containers under one web UI.
- **Headless by design.** No desktop environment is installed on the host — administration happens through the built-in web UI (`https://<ip>:8006`) and SSH. VMs with graphical interfaces get their screens through the noVNC console in the browser.
- **ZFS built in.** The storage strategy (one pool, datasets per purpose, bind-mounts into LXCs) runs on ZFS, which Proxmox supports natively down to the installer.
- **Debian underneath.** Everything learned in the Ubuntu phase of the cluster transfers directly — same ecosystem, same tooling.

---

## Installations

Installer images and version notes live under [`./installations`](./installations):

- [Proxmox VE](./installations/proxmox-ve) — ISO metadata and the macOS bootable-USB workflow

Large ISO files stay out of Git — the repository tracks version, source URL and checksum only.

## After the Installation

- [First Steps](./first-steps.md) — repositories, first update, reboot: the mandatory post-install routine

---

## Decision Log

| Date | Decision |
|---|---|
| 2026-07-27 | Proxmox VE installed on the MS-01 as `pve0`. Headless operation, web UI + SSH only. Management IP static outside the router's DHCP pool. |
