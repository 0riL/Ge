import base64
import os
import requests

def auto_push_to_github(filepath):
    token = os.getenv("GITHUB_PAT")
    repo = os.getenv("GITHUB_REPO")  # Format: username/reponame
    branch = os.getenv("GITHUB_BRANCH", "main")  # Optional: defaults to main

    if not token or not repo:
        print("[GitHub Sync] Missing GITHUB_PAT or GITHUB_REPO environment variables.")
        return

    headers = {
        "Authorization": f"token {token}",
        "Accept": "application/vnd.github.v3+json",
    }

    filename = os.path.basename(filepath)
    url = f"https://api.github.com/repos/{repo}/contents/{filename}"

    try:
        with open(filepath, "rb") as file:
            content = base64.b64encode(file.read()).decode("utf-8")

        # Check if file exists (get SHA)
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            sha = response.json().get("sha")
            data = {
                "message": f"Update {filename}",
                "content": content,
                "branch": branch,
                "sha": sha
            }
        else:
            data = {
                "message": f"Create {filename}",
                "content": content,
                "branch": branch
            }

        put_response = requests.put(url, headers=headers, json=data)

        if put_response.status_code in [200, 201]:
            print(f"[GitHub Sync] Successfully pushed: {filename}")
        else:
            print(f"[GitHub Sync] Failed to push. Status: {put_response.status_code}")
            print(put_response.json())

    except Exception as e:
        print(f"[GitHub Sync] Error: {str(e)}")
