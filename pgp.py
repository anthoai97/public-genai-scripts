import sys
from pgpy import PGPKey

def check_encryption_capability(key_file):
    try:
        # Load the public key
        with open(key_file, "r") as f:
            key_data = f.read()
        
        key, _ = PGPKey.from_blob(key_data)

        # Check primary key usage
        if "Encrypt" in key.key_usage:
            print("✅ Primary key supports encryption!")
            return True

        # Check subkeys
        for subkey in key.subkeys.values():
            if "Encrypt" in subkey.key_usage:
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
