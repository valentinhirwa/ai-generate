"""Simple lesson: how to call the GitHub REST API (https://api.github.com).

Run:  python3 example.py            (uses the user "octocat")
      python3 example.py torvalds   (any GitHub username)

No packages needed, only Python's standard library.
"""
import json
import sys
import urllib.error
import urllib.request

BASE_URL = "https://api.github.com"


def get_json(path):
    """Step 1: send an HTTP GET request and turn the JSON reply into Python data."""
    request = urllib.request.Request(
        BASE_URL + path,
        headers={
            "Accept": "application/vnd.github+json",  # ask for JSON
            "User-Agent": "api-learning-example",     # GitHub requires a User-Agent
            # For private data or higher rate limits add:
            # "Authorization": "Bearer YOUR_TOKEN",
        },
    )
    with urllib.request.urlopen(request, timeout=10) as response:
        return json.load(response)


def main():
    username = sys.argv[1] if len(sys.argv) > 1 else "octocat"

    try:
        # Step 2: GET /users/{username} -> profile info
        user = get_json(f"/users/{username}")
        print(f"Name:         {user['name']}")
        print(f"Public repos: {user['public_repos']}")
        print(f"Followers:    {user['followers']}")

        # Step 3: GET /users/{username}/repos -> list of repositories
        repos = get_json(f"/users/{username}/repos?per_page=5&sort=updated")
        print("\nLatest 5 repositories:")
        for repo in repos:
            print(f"  - {repo['name']} (stars: {repo['stargazers_count']})")

    except urllib.error.HTTPError as error:
        # Step 4: handle errors. 404 = not found, 403 = rate limit reached.
        print(f"API error {error.code}: {error.reason}")
    except urllib.error.URLError as error:
        print(f"Network problem: {error.reason}")


if __name__ == "__main__":
    main()
