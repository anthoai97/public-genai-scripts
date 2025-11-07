import redis
import getpass
import sys

def test_redis_connection(host, port, password, use_ssl):
    """
    Attempts to connect to Redis using host, port, password, and SSL.
    """
    print(f"\nAttempting to connect to host: {host} on port: {port} (SSL: {use_ssl})...")
    
    try:
        # 1. Create the Redis connection object using separate parameters.
        #    This is different from the 'from_url' method.
        r = redis.Redis(
            host=host,
            port=port,
            password=password,
            ssl=use_ssl,  # Set to True for SSL connections (e.g., rediss://)
            decode_responses=True
        )
        
        # 2. Test the connection by sending a PING command.
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
        print(f"\n❌ ConnectionError: Connection failed. Please check your host, port, and network.")
        print(f"   Details: {e}")
    except Exception as e:
        print(f"\n❌ An unexpected error occurred: {e}")
        print(f"   Error type: {type(e).__name__}")

# --- Main execution ---
if __name__ == "__main__":
    try:
        # 1. Get the Redis Host
        host = input("Enter your Redis Host (e.g., my-redis-host.com): ")
        if not host:
            print("Host cannot be empty.")
            sys.exit(1)

        # 2. Get the Port (with a default)
        port_input = input("Enter your Redis Port [default: 6379]: ")
        port = int(port_input) if port_input else 6379
        
        # 3. Check for SSL (common for cloud providers)
        ssl_input = input("Use SSL? (y/n) [default: n]: ").lower()
        use_ssl = ssl_input == 'y'

        # 4. Get the password securely
        password = getpass.getpass("Enter your Redis Password: ")
        
        # 5. Run the connection test
        test_redis_connection(host, port, password, use_ssl)
            
    except KeyboardInterrupt:
        print("\nTest cancelled by user.")
        sys.exit(0)
    except ValueError:
        print("\n❌ Error: Invalid port. Please enter a number.")
        sys.exit(1)
