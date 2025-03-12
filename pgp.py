from pgpy import PGPKey
import sys

def check_encryption_capability(key_file):
    try:
        # Load the public key
        with open(key_file, "r") as f:
            key_data = f.read()
        
        key = PGPKey.from_blob(key_data)[0]

        # Check if the primary key or any subkey supports encryption
        if key.can_encrypt:
            print("✅ Encryption key found!")
            return True

        for subkey in key.subkeys.values():
            if subkey.can_encrypt:
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
