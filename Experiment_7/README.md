# Experiment 7: Analysis of WPA2 Four-Way Handshake with Wireshark

## Aim
To examine a WPA2 four-way EAPOL handshake in Wireshark and study the parameters exchanged between the wireless access point and client.

## Tools Used
- Wireshark
- `Network_Join_Nokia_Mobile.pcap`

## Theory
The WPA2 four-way handshake establishes the required session keys between a client and access point. EAPOL-Key messages carry values such as nonces, MICs, and replay counters during this process.

## Methodology

1. Load the supplied PCAP file in Wireshark.
2. Use the display filter:
   ```text
   eapol
   ```
3. Locate the complete sequence of four EAPOL-Key messages.
4. Use these frames for analysis:
   - Message 1: Frame 726
   - Message 2: Frame 728
   - Message 3: Frame 733
   - Message 4: Frame 738
5. Open **802.1X Authentication → Key Descriptor** in each packet.
6. Note the Key Information, Nonce, MIC, and Replay Counter.
7. Examine the communication direction between the AP and client.
8. Confirm that all four handshake messages are present.

## Handshake Visualization

```text
        Siemens AP                         Nokia Client
             |                                  |
             |-------- 1. ANonce -------------->|
             |          Replay: 0               |
             |                                  |
             |<------- 2. SNonce + MIC ---------|
             |          Replay: 0               |
             |                                  |
             |-------- 3. ANonce + MIC -------->|
             |          Replay: 1               |
             |                                  |
             |<----------- 4. MIC --------------|
             |          Replay: 1               |
             |                                  |
             +---------- Complete --------------+
```

## Results

| Message | Frame | Direction | Replay Counter | Nonce | MIC |
|---|---:|---|---:|---|---|
| 1 of 4 | 726 | Siemens → Nokia | 0 | ANonce | Zero |
| 2 of 4 | 728 | Nokia → Siemens | 0 | SNonce | Present |
| 3 of 4 | 733 | Siemens → Nokia | 1 | ANonce | Present |
| 4 of 4 | 738 | Nokia → Siemens | 1 | Zeroed | Present |

Frame 728 also contained the WPA Information Element indicating TKIP for the multicast and unicast cipher suites and PSK for authentication/key management.

## Discussion
Analysis of the capture confirmed the complete four-message WPA2 EAPOL exchange. The packets demonstrated the exchange of nonces, MIC values, and replay counters required during the handshake.

## Output
The WPA2 four-way handshake was successfully analyzed using Wireshark and the relevant EAPOL-Key parameters were recorded.

## Screenshots
1. Complete `eapol` filtered packet list.
2. Frame 726 showing Message 1.
3. Frame 728 showing Message 2.
4. Frame 733 showing Message 3.
5. Frame 738 showing Message 4.
