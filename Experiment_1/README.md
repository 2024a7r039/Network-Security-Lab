# Experiment 1: Classical Symmetric Ciphers

## Aim

To implement Caesar Cipher and Vigenère Cipher in Python for encryption and decryption.

## Methodology

### Caesar Cipher

- Accept plaintext and shift value from the user.
- Shift each alphabetic character using modulo 26.
- Preserve uppercase and lowercase characters.
- Preserve spaces and special characters.
- Decrypt by applying the negative of the encryption shift.

### Vigenère Cipher

- Accept plaintext and an alphabetic key.
- Convert each key character into a shift value.
- Repeat the key throughout the plaintext.
- Apply the key only to alphabetic characters.
- Preserve spaces, punctuation, and character case.
- Subtract the same shifts during decryption.

## Features

- Menu-driven interface
- Caesar encryption and decryption
- Vigenère encryption and decryption
- User-defined shift
- User-defined key
- Case preservation
- Special-character preservation
- Vigenère key alignment across spaces

## Results

Both ciphers successfully performed encryption and decryption.

| Cipher | Encryption | Decryption | Verification |
|--------|------------|------------|--------------|
| Caesar | Successful | Successful | Passed |
| Vigenère | Successful | Successful | Passed |

The decrypted text matched the original plaintext in the tested cases.

## Discussion

Caesar Cipher uses a fixed shift and has a small key space, making it easy to brute-force.

Vigenère Cipher uses multiple shifts through a repeating key, providing better protection against simple frequency analysis. However, the repeating-key pattern can still be exploited for longer messages.

## Improvements

- Added a menu-driven interface.
- Added runtime input for plaintext, shift, and key.
- Added automatic encryption and decryption verification.
- Preserved uppercase and lowercase characters.
- Preserved spaces and special characters.
- Used a separate key index for correct Vigenère key alignment.
