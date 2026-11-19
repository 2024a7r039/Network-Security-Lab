# Network Security Lab — Experiment 10
## Intrusion Detection and Packet Filtering with pfSense & Snort

### Purpose of the Lab
The goal of this experiment is to build a segmented virtual network protected by **pfSense** and **Snort IDS**. By combining stateful firewall Access Control Lists (ACLs) with signature-based deep packet inspection, we evaluate how legitimate traffic is permitted while unauthorized port probes, brute-force attacks, and floods are blocked and alerted.

---

### Testbed Environment

All three virtual machines communicate over an isolated host/internal virtual switch (`192.168.1.0/24`):

* **Gateway Firewall & IDS (`pfSense 2.8.1`):** Routes traffic between WAN (`em0`) and the internal LAN (`em1` at `192.168.1.1/24`), hosting the Snort IDS sensor.
* **Simulated Threat Actor (`Kali Linux` — `192.168.1.10`):** Generates both benign HTTP requests and controlled network attacks.
* **Target Host (`Metasploitable 2` — `192.168.1.20`):** Runs vulnerable network services (Apache HTTP, FTP, Telnet) to test perimeter defenses.

---

### Deployment Workflow

#### Phase 1: Firewall & Network Setup
1. Installed pfSense and mapped `em0` to **WAN (NAT)** and `em1` to **LAN (`192.168.1.1/24`)** with DHCP enabled.
2. Logged into the pfSense administrative interface (`https://192.168.1.1`) from the internal network.
3. Replaced the default open LAN rule with a strict whitelist under **Firewall $\rightarrow$ Rules $\rightarrow$ LAN**:
   * **Allow** TCP Port `80` (HTTP) from `LAN net`
   * **Allow** TCP Port `443` (HTTPS) from `LAN net`
   * **Allow** UDP Port `53` (DNS) from `LAN net`
   * **Block** all remaining traffic (`Protocol: any`, placed at the bottom of the rule table)

#### Phase 2: Enabling Snort IDS
1. Navigated to **System $\rightarrow$ Package Manager** and installed the **Snort** package.
2. Configured Snort on the **LAN** interface (**Services $\rightarrow$ Snort**), downloaded and enabled Emerging Threats / Community rule categories, and started the Snort service.

---

### Testing & Validation Results

#### 1. Verification of Firewall Policy
* **Authorized Web Access:** Running `curl -I http://192.168.1.20` from Kali successfully retrieved `HTTP/1.1 200 OK` from Metasploitable's Apache server, confirming the TCP 80 pass rule functioned properly.
* **Unauthorized Service Block:** Running `telnet 192.168.1.20 23` failed to connect, and **Status $\rightarrow$ System Logs $\rightarrow$ Firewall** confirmed the packet was dropped by the catch-all block rule.

#### 2. Verification of Snort IDS Alerts
Controlled offensive tests were launched from Kali Linux (`192.168.1.10`) toward Metasploitable 2 (`192.168.1.20`):

| Attack Type | Command Executed on Kali | Observed Defensive Behavior |
| :--- | :--- | :--- |
| **Port Scan** | `nmap -p 1-1000 192.168.1.20` | Snort logged `[ET SCAN]` reconnaissance alerts; non-whitelisted ports were filtered by pfSense. |
| **Credential Brute-Force** | `hydra -l msfadmin -P /usr/share/wordlists/rockyou.txt ftp://192.168.1.20` | Snort generated `[ET POLICY] FTP Brute Force` alerts identifying the source/target pair. |
| **ICMP Flood** | `ping -f 192.168.1.20` | Snort flagged anomalous ICMP packet rates in **Services $\rightarrow$ Snort $\rightarrow$ Alerts**. |

---

### Conclusion
Combining pfSense's stateful packet filter with Snort's signature inspection establishes defense-in-depth: pfSense enforces strict port-level access control at the perimeter, while Snort provides visibility into suspicious traffic patterns and active exploitation attempts across the network.
