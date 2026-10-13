# Experiment 5: TLS Handshake Capture and Analysis

## Aim

To monitor an HTTPS connection with Wireshark and analyze the TLS handshake, including the messages exchanged between the client and server, negotiated security parameters, and server certificate.

## Theory

TLS establishes a protected communication channel by negotiating cryptographic settings, authenticating the server, and creating session keys. During the handshake, the client proposes supported options and the server selects the parameters that will be used.

In TLS 1.3, handshake messages after ServerHello are normally protected, so a browser TLS key log can be used when further packet-level inspection is required.

## Tools and Technologies

- Wireshark
- Web Browser
- HTTPS
- TLS 1.3
- SSLKEYLOGFILE
- PCAPNG packet capture

## Objective

1. Capture an HTTPS session over TCP port 443.
2. Locate the ClientHello and ServerHello packets.
3. Examine the options proposed by the client.
4. Determine the parameters selected by the server.
5. Examine the server certificate.
6. Study the protected portion of the TLS 1.3 handshake.

## Methodology

### 1. Select Network Interface

Wireshark was opened and the interface showing active network traffic was selected.

### 2. Capture HTTPS Packets

The following capture filter was applied:

```text
tcp port 443
```

A fresh private browser window was then used to access:

```text
https://www.wireshark.org/
```

### 3. Save the Capture

After the connection was established, the capture was stopped and saved as:

```text
exp5_tls_handshake.pcapng
```

### 4. Display TLS Packets

The captured traffic was filtered using:

```text
tls
```

### 5. Examine ClientHello

The ClientHello was located with:

```text
tls.handshake.type == 1
```

The packet was checked for the requested hostname, supported versions, cipher-suite list, and key-share extension.

### 6. Examine ServerHello

The ServerHello was located with:

```text
tls.handshake.type == 2
```

The selected TLS version, cipher suite, and key-share group were then recorded.

### 7. Enable Key Logging

For analysis of encrypted TLS 1.3 messages, the browser can be started with the following configuration.

#### Windows

```cmd
@echo off
set SSLKEYLOGFILE=%USERPROFILE%\Desktop\tls-keys.log
start firefox
```

#### Linux

```bash
export SSLKEYLOGFILE=$HOME/Desktop/tls-keys.log
firefox
```

#### macOS

```bash
export SSLKEYLOGFILE=$HOME/Desktop/tls-keys.log
open -a firefox
```

### 8. Configure TLS Decryption

In Wireshark, the key-log file is supplied under:

```text
Edit → Preferences → Protocols → TLS
```

A new HTTPS session is captured after configuring the key log.

### 9. Examine Protected Messages

The following filter can be used:

```text
tls.handshake.type == 8 ||
tls.handshake.type == 11 ||
tls.handshake.type == 15 ||
tls.handshake.type == 20
```

### 10. Examine the Certificate

The certificate can be opened through:

```text
Transport Layer Security
→ Handshake Protocol: Certificate
→ Certificates
→ signedCertificate
```

The subject, issuer, SAN, validity, public-key information, and chain can then be recorded.

## Wireshark Filters Used

### Capture Filter

```text
tcp port 443
```

### TLS Filter

```text
tls
```

### ClientHello

```text
tls.handshake.type == 1
```

### ServerHello

```text
tls.handshake.type == 2
```

### Certificate

```text
tls.handshake.type == 11
```

### Protected Handshake

```text
tls.handshake.type == 8 ||
tls.handshake.type == 11 ||
tls.handshake.type == 15 ||
tls.handshake.type == 20
```

## Results

The HTTPS traffic was captured successfully and the main TLS handshake packets were identified.

| Parameter | Observation |
|---|---|
| Protocol Version | `TLS 1.3` |
| Test Host | `www.wireshark.org` |
| Certificate Common Name | `wireshark.org` |
| Certificate Issuer | `WE1, Google Trust Services` |
| Selected Cipher Suite | To be obtained from ServerHello |

The certificate examined during the experiment showed a validity period from 22 August 2026 to 20 November 2026.

## Discussion

The packet analysis showed the negotiation process between the client and server. The client sends its supported options in ClientHello, and the server responds with the parameters selected for the connection.

The certificate is used to authenticate the server, while TLS 1.3 protects the later handshake messages after ServerHello.

## Improvements

- Use a separate HTTPS session to keep the capture focused.
- Verify negotiated parameters directly from ServerHello.
- Enable key logging when encrypted handshake details must be inspected.
- Remove the temporary key log after the experiment.

## TLS Handshake Flow

```text
Client                                      Server
  │                                           │
  │ ----------- ClientHello ----------------> │
  │                                           │
  │ <----------- ServerHello ---------------- │
  │                                           │
  │ <-------- EncryptedExtensions ----------- │
  │ <------------- Certificate ------------- │
  │ <---------- CertificateVerify ---------- │
  │ <--------------- Finished -------------- │
  │                                           │
  │ -------------- Finished ---------------> │
  │                                           │
  │ <------ Encrypted Application Data ----> │
```

## Output

The following evidence was obtained or is required for the experiment:

1. ClientHello packet
2. ServerHello packet
3. Selected TLS parameters
4. Server certificate information
5. TLS handshake screenshots
6. `exp5_tls_handshake.pcapng`

### Screenshots

- ClientHello packet with expanded details
- ServerHello showing selected parameters
- Certificate information
- Decrypted TLS handshake messages, if key logging is enabled

## Safety and Notes

- Only authorized traffic should be captured.
- Avoid personal accounts during packet collection.
- Use a fresh private browser session.
- Treat the TLS key log as sensitive information.
- Remove the key log after the experiment.

## Conclusion

The TLS session was captured and examined with Wireshark. The experiment demonstrated how TLS 1.3 negotiates connection parameters, authenticates the server through a certificate, and protects the subsequent handshake and application communication.
