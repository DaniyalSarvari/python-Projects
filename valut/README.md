# Vault - CLI Password Manager

Encrypted local password manager using Fernet symmetric encryption.

## Security

- AES-128-CBC encryption via Fernet
- PBKDF2 key derivation with SHA256 and 480,000 iterations
- Passwords never stored in plain text

## Setup

```bash
pip install cryptography
python3 vault.py init
python3 vault.py
