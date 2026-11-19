# COM-511 Network Security Lab — Experiment 9
## Configuring and Analyzing an IKEv2 IPsec Tunnel (`strongSwan` & Linux XFRM)

### Overview
In this lab exercise, we constructed a two-gateway IPsec VPN operating in **Tunnel Mode** between a Kali Linux peer (**Gateway A**) and an Ubuntu Linux peer (**Gateway B**). Using **IKEv2** (`strongSwan 6.x` with `swanctl`), both gateways authenticated via a shared cryptographic secret, dynamically derived session keys, and programmed the Linux kernel's **XFRM** framework to protect traffic passing between simulated private networks (`10.10.1.1/32` and `10.20.1.1/32`).

---

### Lab Architecture & Role Assignment

| Attribute | Gateway B (Local Node — Ubuntu) | Gateway A (Remote Peer — Kali) |
| :--- | :--- | :--- |
| **Role** | IKEv2 Responder | IKEv2 Initiator |
| **Physical/Virtual NIC** | `ens34` | `eth1` |
| **Outer Tunnel IP** | `192.168.159.145/24` | `192.168.159.140/24` |
| **Simulated Private Subnet** | `10.20.1.1/32` (on `lo`) | `10.10.1.1/32` (on `lo`) |
| **Peer Identifier** | `gw-b` | `gw-a` |
| **IKEv2 Cipher Suite** | `AES-256-GCM-16` / `PRF-SHA256` / `MODP-3072` | `AES-256-GCM-16` / `PRF-SHA256` / `MODP-3072` |
| **CHILD SA Cipher Suite** | `ESP: AES-256-GCM-16` (Tunnel Mode) | `ESP: AES-256-GCM-16` (Tunnel Mode) |

---

### Setup & Configuration Walkthrough

#### 1. Service Installation & Loopback Provisioning
Because modern strongSwan releases deprecate the legacy `ipsec` stroke interface, `charon-systemd` and `strongswan-swanctl` were deployed alongside `tcpdump`. On Ubuntu (Gateway B), loopback alias `10.20.1.1/32` was configured to represent the protected internal host:

```bash
sudo apt update && sudo apt install -y charon-systemd strongswan-swanctl tcpdump
sudo systemctl enable --now strongswan
sudo ip address add 10.20.1.1/32 dev lo
```

#### 2. Responder Configuration (`/etc/swanctl/swanctl.conf`)
To establish a symmetric tunnel, Gateway B's local and remote parameters mirror Gateway A's configuration. The shared 256-bit+ Base64 secret is prefixed with `0s` and sanitized below for security:

```ini
connections {
  lab-vpn {
    version = 2
    local_addrs = 192.168.159.145
    remote_addrs = 192.168.159.140
    proposals = aes256gcm16-prfsha256-modp3072

    local {
      auth = psk
      id = gw-b
    }
    remote {
      auth = psk
      id = gw-a
    }

    children {
      lab-net {
        local_ts = 10.20.1.1/32
        remote_ts = 10.10.1.1/32
        esp_proposals = aes256gcm16
      }
    }
  }
}

secrets {
  ike-lab {
    secret = 0s<PSK_REMOVED_FOR_SUBMISSION>
  }
}
```

#### 3. Loading Policies & Handling Tunnel Negotiation
After restricting file permissions (`chmod 600`) and loading the configuration via `sudo swanctl --load-all`, Gateway B listened on UDP ports `500` and `4500` and automatically responded to Gateway A's `IKE_SA_INIT` and `IKE_AUTH` requests.

---

### Verification & Packet Capture Findings

#### 1. Control & Data Plane Verification
* **Connection Table (`sudo swanctl --list-conns`):** Confirmed `lab-vpn` loaded with `IKEv2` and `lab-net` configured for `TUNNEL` mode between `10.20.1.1/32` (local) and `10.10.1.1/32` (remote).
* **Active Security Associations (`sudo swanctl --list-sas`):** Verified `IKE_SA` state as `ESTABLISHED` and `CHILD_SA` state as `INSTALLED` with bidirectional Security Parameter Indices (`0xc807675e` and `0xc6ec928a`).
* **Kernel XFRM Tables (`sudo ip xfrm state` & `policy`):** Confirmed the kernel installed `rfc4106(gcm(aes))` AEAD transformation states and inbound/outbound/forward policies matching the `10.20.1.1/32` $\leftrightarrow$ `10.10.1.1/32` selectors.

#### 2. End-to-End Connectivity & SA Counter Validation
Executing an ICMP echo test bound to the inner loopback interface from Ubuntu to Kali verified tunnel encapsulation:

```bash
ping -I 10.20.1.1 -c 4 10.10.1.1
# 4 packets transmitted, 4 received, 0% packet loss, rtt avg = 0.478 ms
```
Following bidirectional pings (8 ICMP requests + 8 replies total), the CHILD SA packet counters increased from `0` to `8 packets (672 bytes)` inbound and `8 packets (672 bytes)` outbound, proving that kernel XFRM intercepted and encrypted the traffic.

#### 3. Wireshark Traffic Analysis (`isakmp || esp || ah`)
Inspecting the outer-link `.pcap` capture confirmed the structural behavior of IPsec Tunnel Mode:
* **Phase 1 & 2 Negotiation (`ISAKMP`):** Packets 1–4 captured the `IKE_SA_INIT` exchange (plaintext cryptographic parameter negotiation and DH key exchange) followed by `IKE_AUTH` (encrypted peer authentication and CHILD SA setup).
* **Encapsulated Data (`ESP`):** Packets 5–20 appeared strictly as **IP Protocol 50 (ESP)** frames between `192.168.159.140` and `192.168.159.145`. While outer IP headers, SPIs, sequence numbers, and frame lengths (`154 bytes`) remain observable on the wire, the entire original IP packet (`10.20.1.1` $\rightarrow$ `10.10.1.1`) and its ICMP payload are encrypted.
* **Absence of `AH`:** Filtering for Authentication Header (`ah`) returned zero frames because `AES-GCM-16` inside ESP already provides Authenticated Encryption with Associated Data (AEAD).

---

### Post-Lab Restoration
To return the Ubuntu VM to its baseline network state after capturing evidence:
```bash
sudo ip address del 10.20.1.1/32 dev lo
```
