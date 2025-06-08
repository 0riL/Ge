import base64
import json
import requests
import time
from config import GITHUB_PAT, GITHUB_REPO, GITHUB_BRANCH

def push_to_github(local_file_path, repo_path):
    try:
        url = f"https://api.github.com/repos/{GITHUB_REPO}/contents/{repo_path}"
        headers = {
            "Authorization": f"token {GITHUB_PAT}",
            "Accept": "application/vnd.github.v3+json",
        }

        # Check if file exists
        get_resp = requests.get(url, headers=headers)
        sha = get_resp.json().get("sha", None)

        with open(local_file_path, "rb") as f:
            content = base64.b64encode(f.read()).decode("utf-8")

        payload = {
            "message": f"Auto-update {repo_path}",
            "content": content,
            "branch": GITHUB_BRANCH,
        }

        if sha:
            payload["sha"] = sha

        resp = requests.put(url, headers=headers, json=payload)
        if resp.status_code not in [200, 201]:
            print("❌ GitHub sync failed:", resp.json())
    except Exception as e:
        print("❌ GitHub push error:", e)
