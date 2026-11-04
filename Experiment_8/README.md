# Experiment 8: Protected Email Exchange with OpenPGP and Thunderbird

## Objective

Use Thunderbird's OpenPGP support to exchange email in both directions, protecting message content with encryption and checking sender signatures.

## Account and key record

| Participant | Address / shown name | Key ID |
|---|---|---|
| Harleen | `2024a7r039@mietjammu.in` | `0x12DE1760A3ABF8CA` |
| Correspondent | `lightsingy123@gmail.com` (Aakriti Singh) | `0xC0C83C39934244E2` |

## Message path at a glance

```text
Harleen                                                Aakriti Singh
Harleen private key                                    Aakriti private key
      |                                                       |
      |<------ public-key exchange / identity check --------->|
      |                                                       |
      | encrypt to Aakriti + sign as Harleen                 |
      |------------------------------------------------------>|
      |                                       decrypt + validate signature
      |                                                       |
      | encrypt to Harleen + sign as Aakriti                 |
      |<------------------------------------------------------|
      | decrypt + validate signature                         |
```

## Workflow

1. Set up/select the OpenPGP key pair associated with Harleen's Thunderbird account and provide the public key to the correspondent.
2. Import the correspondent's public key into Thunderbird. Check the full fingerprint with the correspondent over a trusted channel; do not treat the short key ID as identity verification.
3. For the outgoing message, address Aakriti Singh and turn on both encryption and digital signing. Send the message.
4. The recipient uses their private key to decrypt and Thunderbird checks the signature using Harleen's public key.
5. For the return message, the correspondent signs and encrypts for Harleen. Harleen decrypts the received message and inspects Thunderbird's security details for the encryption and signature results.

## Results recorded from the screenshots

| Message direction | Message opened successfully | Signature verification | Associated key IDs |
|---|---|---|---|
| Harleen → Aakriti Singh | Yes: encryption/decryption successful | Valid | Harleen `0x12DE1760A3ABF8CA`; correspondent `0xC0C83C39934244E2` |
| Aakriti Singh → Harleen | Yes: encryption/decryption successful | Valid | Correspondent `0xC0C83C39934244E2`; Harleen `0x12DE1760A3ABF8CA` |

The conversation reports successful encryption/decryption and valid signatures for both directions. Exact message contents, dates, algorithms, and fingerprint strings were not captured in the written observations.

## What the result means

Encryption provides confidentiality for the intended recipient, who can decrypt with the matching private key. The verified signature supports message integrity and confirms that the message matches a signature made by the private key corresponding to the public key Thunderbird checked. To connect that key to Aakriti or Harleen personally, the fingerprint must be verified out of band. The observed key IDs are useful for distinguishing keys, but do not prove identity on their own.

## Evidence to include

- [ ] Harleen's sent-message security view: encrypted message and valid signature.
- [ ] Harleen's received-reply security view: successful decryption and valid signature.
- [ ] Key details for Harleen: `0x12DE1760A3ABF8CA`.
- [ ] Key details for the correspondent: `0xC0C83C39934244E2`.
- [ ] Fingerprint verification evidence if demanded by the experiment handout; no fingerprint is stated in the supplied observations.

## Conclusion

Harleen and Aakriti Singh completed a successful two-way OpenPGP email exchange in Thunderbird. Both received messages were decrypted successfully, and each direction showed a valid digital signature, demonstrating confidentiality and signature validation for the keys used.
