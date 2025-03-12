import sys
from pgpy import PGPKey

# Algorithms that support encryption
ENCRYPTION_ALGORITHMS = {
    1, 2, 3,    # RSA (Encrypt/Sign, Encrypt-Only, Sign-Only)
    16, 20,     # ElGamal (Encrypt-Only)
    18          # ECDH (Elliptic Curve Diffie-Hellman)
}

def check_encryption_capability(key_file):
    try:
        # Load the public key
        with open(key_file, "r") as f:
            key_data = f.read()
        
        key, _ = PGPKey.from_blob(key_data)

        # Check primary key algorithm
        if key.key_algorithm in ENCRYPTION_ALGORITHMS:
            print("✅ Primary key supports encryption!")
            return True

        # Check subkeys for encryption support
        for subkey in key.subkeys.values():
            if subkey.key_algorithm in ENCRYPTION_ALGORITHMS:
                print("✅ Encryption subkey found!")
                return True

        print("❌ No encryption key found. Key is for signing only.")
        return False

    except Exception as e:
        print(f"Error: {e}")
        return False

# Usage
if len(sys.argv) != 2:
    print("Usage: python check_gpg_key.py <public-key-file>")
    sys.exit(1)

key_file = sys.argv[1]
check_encryption_capability(key_file)
