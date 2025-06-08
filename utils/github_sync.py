import base64
import os
import requests

def auto_push_to_github(filepath):
    token = os.getenv("GITHUB_PAT")
    repo = os.getenv("GITHUB_REPO")
    if not token or not repo:
        return
    headers = {
        "Authorization": f"token {token}",
        "Accept": "application/vnd.github.v3+json",
    }
    filename = os.path.basename(filepath)
    url = f"https://api.github.com/repos/{'/'.join(repo.split('/')[-2:])}/contents/{filename}"

    with open(filepath, 'rb') as f:
        content = base64.b64encode(f.read()).decode()

    get_response = requests.get(url, headers=headers)
    if get_response.status_code == 200:
        sha = get_response.json().get("sha")
        data = {
            "message": f"Update {filename}",
            "content": content,
            "sha": sha
        }
    else:
        data = {
            "message": f"Create {filename}",
            "content": content
        }

    requests.put(url, headers=headers, json=data)
