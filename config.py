import os

GITHUB_PAT = os.getenv("GITHUB_PAT")
GITHUB_REPO = os.getenv("GITHUB_REPO")  # format: username/repo
GITHUB_BRANCH = os.getenv("GITHUB_BRANCH", "main")
BOT_SPEED = int(os.getenv("BOT_SPEED", "1"))  # usernames per second
