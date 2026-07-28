# pfSense

[← Back to Router & Firewall](../README.md)

pfSense is the best-known open-source firewall distribution and the project [OPNsense](../opnsense) was forked from in 2015. Both are FreeBSD-based, both do routing, stateful firewalling, DHCP, DNS and VPN, and both are administered through a web interface. For most homelabs either one would work.

It is documented here as the **main alternative**, because any honest router decision has to compare these two.

---

## Why It Is Documented

- It is the reference point: most homelab firewall tutorials, forum answers and hardware guides are written for pfSense.
- Its plugin ecosystem and long history mean a solution exists for almost every scenario.
- Netgate, the company behind it, sells matching appliances — a relevant option for anyone who wants a physical firewall instead of a virtual machine.

---

## Why It Is Not Chosen

- **Community edition versus paid edition.** Netgate maintains pfSense CE alongside pfSense Plus, and the more polished features have been landing on the commercial side. OPNsense keeps one edition for everyone.
- **Release cadence.** OPNsense ships predictable, frequent releases; pfSense CE updates arrive more slowly and less predictably.
- **API and automation.** OPNsense exposes a documented REST API as a first-class feature, which fits this project's "configuration as code" goal better.
- **Interface.** OPNsense's rewritten UI is the more approachable starting point for someone building a first serious zone model.

None of these are disqualifying. The choice is a preference for the more open, faster-moving fork — not a verdict against pfSense.

---

## Comparison Notes

| System | Best at | Trade-off |
|---|---|---|
| [OPNsense](../opnsense) | Open development, REST API, frequent releases (chosen here) | Smaller ecosystem than pfSense |
| pfSense CE | Huge community, endless documentation, matching appliances | Two-tier product strategy, slower releases |
| OpenWrt | Small hardware, low resource use | Weaker multi-VLAN firewall ergonomics |
| RouterOS (CHR) | One ecosystem with the MikroTik switch | Steep learning curve, unfriendly firewall model |

---

## Runtime Status

`⚫ Inactive` and not planned. [OPNsense](../opnsense) is the chosen router; this page exists for comparison.

---

## Documentation

- [pfSense documentation](https://docs.netgate.com/pfsense/en/latest/)
- [Wikipedia: pfSense](https://en.wikipedia.org/wiki/PfSense)
