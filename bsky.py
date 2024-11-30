import requests
from colorama import Fore, Style, init

# Initialize colorama for Windows compatibility
init(autoreset=True)

# URL of the pastebin containing the username list
pastebin_url = "https://raw.githubusercontent.com/coneticc/ogwords/refs/heads/main/words.txt"

# Bluesky API endpoint
api_endpoint = "https://public.api.bsky.app/xrpc/com.atproto.identity.resolveHandle?handle="

def fetch_usernames(pastebin_url):
    """Fetch usernames from the pastebin URL."""
    response = requests.get(pastebin_url)
    if response.status_code == 200:
        return response.text.splitlines()
    else:
        print(f"Failed to fetch usernames. Status code: {response.status_code}")
        return []

def check_username_availability(username):
    """Check the availability of a username using the Bluesky API."""
    url = f"{api_endpoint}{username}.bsky.social"
    response = requests.get(url)
    if response.status_code == 200:
        if "did" in response.json():
            return "Unavailable"
    elif response.status_code == 400:  # Error for unavailable profiles
        error_data = response.json()
        if error_data.get("error") == "InvalidRequest" and "Unable to resolve handle" in error_data.get("message", ""):
            return "Available"
    return "Unknown"

def main():
    usernames = fetch_usernames(pastebin_url)
    results = {"Available": [], "Unavailable": [], "Unknown": []}

    for username in usernames:
        status = check_username_availability(username)
        results[status].append(username)
        if status == "Available":
            print(f"{Fore.GREEN}{username}: {status}{Style.RESET_ALL}")
        elif status == "Unavailable":
            print(f"{Fore.RED}{username}: {status}{Style.RESET_ALL}")
        else:
            print(f"{username}: {status}")

    # Print summary
    print("\nSummary:")
    for status, names in results.items():
        print(f"{status}: {len(names)} usernames")
        for name in names:
            print(f"  - {name}")

if __name__ == "__main__":
    main()
