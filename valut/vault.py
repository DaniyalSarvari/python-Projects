#!/usr/bin/env python3
import os
import sys
import json
import base64
import secrets
import string
import getpass
from getpass import getpass
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC

VAULT_FILE = "vault.enc"
SALT_FILE = "salt.bin"


def generate_salt():
    salt = os.urandom(16)
    with open(SALT_FILE, "wb") as f:
        f.write(salt)
    return salt


def load_salt():
    if not os.path.exists(SALT_FILE):
        return generate_salt()
    with open(SALT_FILE, "rb") as f:
        return f.read()


def derive_key(master_password, salt):
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,
        iterations=480000,
    )
    key = base64.urlsafe_b64encode(kdf.derive(master_password.encode()))
    return key


def load_vault(key):
    if not os.path.exists(VAULT_FILE):
        return {}
    try:
        f = Fernet(key)
        with open(VAULT_FILE, "rb") as file:
            encrypted = file.read()
        decrypted = f.decrypt(encrypted)
        return json.loads(decrypted)
    except Exception:
        print("Wrong master password or corrupted vault.")
        sys.exit(1)


def save_vault(data, key):
    f = Fernet(key)
    encrypted = f.encrypt(json.dumps(data).encode())
    with open(VAULT_FILE, "wb") as file:
        file.write(encrypted)


def generate_password(length=16):
    chars = string.ascii_letters + string.digits + "!@#$%^&*"
    return "".join(secrets.choice(chars) for _ in range(length))


def add_entry(data):
    print("\n--- Add New Entry ---")
    site = input("Site/Service: ").strip()
    username = input("Username: ").strip()
    use_generated = input("Generate password? (y/n): ").strip().lower()

    if use_generated == "y":
        password = generate_password()
        print(f"Generated password: {password}")
    else:
        password = getpass("Password: ")

    url = input("URL (optional): ").strip()
    notes = input("Notes (optional): ").strip()

    data[site] = {
        "username": username,
        "password": password,
        "url": url,
        "notes": notes,
    }
    print(f"Entry for '{site}' added.")


def list_entries(data):
    if not data:
        print("\nVault is empty.")
        return
    print("\n--- Stored Services ---")
    for i, site in enumerate(sorted(data.keys()), 1):
        print(f"{i}. {site}")


def view_entry(data):
    list_entries(data)
    if not data:
        return
    site = input("\nEnter site name: ").strip()
    if site in data:
        entry = data[site]
        print(f"\nSite: {site}")
        print(f"Username: {entry['username']}")
        print(f"Password: {entry['password']}")
        print(f"URL: {entry['url']}")
        print(f"Notes: {entry['notes']}")
    else:
        print("Entry not found.")


def delete_entry(data):
    list_entries(data)
    if not data:
        return
    site = input("\nEnter site name to delete: ").strip()
    if site in data:
        del data[site]
        print(f"Entry for '{site}' deleted.")
    else:
        print("Entry not found.")


def main():
    salt = load_salt()

    if len(sys.argv) > 1 and sys.argv[1] == "init":
        master_password = getpass("Set master password: ")
        confirm = getpass("Confirm master password: ")
        if master_password != confirm:
            print("Passwords do not match.")
            sys.exit(1)
        key = derive_key(master_password, salt)
        save_vault({}, key)
        print("Vault initialized.")
        return

    if not os.path.exists(VAULT_FILE):
        print("No vault found. Run 'python3 vault.py init' to create one.")
        sys.exit(1)

    master_password = getpass("Master password: ")
    key = derive_key(master_password, salt)
    data = load_vault(key)

    while True:
        print("\n" + "-" * 30)
        print("1. Add entry")
        print("2. List entries")
        print("3. View entry")
        print("4. Delete entry")
        print("5. Generate password")
        print("6. Exit")
        choice = input("> ").strip()

        if choice == "1":
            add_entry(data)
            save_vault(data, key)
        elif choice == "2":
            list_entries(data)
        elif choice == "3":
            view_entry(data)
        elif choice == "4":
            delete_entry(data)
            save_vault(data, key)
        elif choice == "5":
            pwd = generate_password()
            print(f"\nGenerated: {pwd}")
        elif choice == "6":
            break
        else:
            print("Invalid choice.")


if __name__ == "__main__":
    main()
