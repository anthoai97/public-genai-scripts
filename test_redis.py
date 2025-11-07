import redis
import getpass
import sys

def test_redis_connection(redis_url, redis_password):
    """
    Attempts to connect to Redis using a URL and password and runs PING.
    """
    print(f"Attempting to connect to: {redis_url}...")
    
    try:
        # 1. Create the Redis connection object from the URL.
        #    decode_responses=True makes the client return strings, not bytes.
        r = redis.Redis.from_url(
            redis_url,
            password=redis_password,
            decode_responses=True
        )
        
        # 2. Test the connection by sending a PING command.
        #    This will raise an exception if the connection or auth fails.
        response = r.ping()
        
        # 3. Check the response.
        if response:
            print("\n✅ Success! Connection established.")
            print(f"Server responded with: {response}") # Should be 'PONG'
        else:
            print("\n⚠️ Connection established, but PING returned an unexpected response.")

    except redis.exceptions.AuthenticationError:
        print("\n❌ AuthenticationError: Connection failed. Please check your password.")
    except redis.exceptions.ConnectionError as e:
        print(f"\n❌ ConnectionError: Connection failed. Please check your URL and network.")
        print(f"   Details: {e}")
    except Exception as e:
        print(f"\n❌ An unexpected error occurred: {e}")
        print(f"   Error type: {type(e).__name__}")

# --- Main execution ---
if __name__ == "__main__":
    try:
        # 1. Get the Redis URL from the user
        url = input("Enter your Redis URL (e.g., redis://localhost:6379/0): ")
        
        # 2. Get the password securely
        #    getpass.getpass() hides the input as the user types
        password = getpass.getpass("Enter your Redis Password: ")
        
        if not url:
            print("URL cannot be empty.")
        else:
            # 3. Run the connection test
            test_redis_connection(url, password)
            
    except KeyboardInterrupt:
        print("\nTest cancelled by user.")
        sys.exit(0)
