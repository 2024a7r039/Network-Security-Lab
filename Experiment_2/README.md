# Experiment 2: SHA-256 Data Integrity

## Aim

To generate SHA-256 hashes for text and files and detect file modifications by comparing hash values.

## Methodology

1. Accept text or a file as input.
2. Generate its SHA-256 hash.
3. Display the file content and its hash.
4. Store the original hash before modification.
5. Append additional text to the file.
6. Generate the hash of the modified file.
7. Compare the original and modified hashes.
8. Display the integrity status.

## Implementation

The program uses Python's `hashlib` module to generate SHA-256 hashes.

The program provides three operations:

- Hash user-provided text.
- Generate the SHA-256 hash of a file.
- Append text to a file and compare its hash before and after modification.

## Features

- SHA-256 text hashing
- SHA-256 file hashing
- File content display
- File modification through text appending
- Original and modified hash comparison
- Automatic integrity status
- File-not-found handling
- Menu-driven interface

## Results

| Operation | Result |
|-----------|--------|
| Text hashing | SHA-256 hash generated |
| File hashing | SHA-256 hash generated |
| Text appended | File modified successfully |
| Hash comparison | Change detected |

A different SHA-256 hash is obtained after text is appended to the file, indicating that the file content has been modified.

## Discussion

SHA-256 produces a fixed-length 256-bit hash represented by 64 hexadecimal characters. Changing the file content results in a different hash value, which can be used to detect modifications.

Hashing verifies data integrity but does not provide data confidentiality.

## Improvements

- Used a common hash-generation function for both text and file data.
- Added automatic calculation of the original file hash.
- Added automatic calculation of the modified file hash.
- Added direct hash comparison after modification.
- Limited the tampering simulation to appending text.
- Added automatic `MODIFIED` or `UNCHANGED` status.
- Added file-not-found handling.
