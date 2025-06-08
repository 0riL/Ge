import os
import json
import asyncio
import aiohttp
import string
import random
import time
from config import BOT_SPEED
from github_sync import push_to_github

CHECKED_FILE = 'username_logs/checked_usernames.json'
REPO_CHECKED_PATH = 'username_logs/checked_usernames.json'

os.makedirs('username_logs', exist_ok=True)

# Load checked usernames
try:
    with open(CHECKED_FILE, 'r') as f:
        checked_usernames = set(json.load(f))
except:
    checked_usernames = set()

def save_usernames():
    with open(CHECKED_FILE, 'w') as f:
        json.dump(list(checked_usernames), f)
    push_to_github(CHECKED_FILE, REPO_CHECKED_PATH)

def generate_username(length=4):
    return ''.join(random.choices(string.ascii_lowercase + string.digits, k=length))

async def check_username(username):
    url = "https://users.roblox.com/v1/usernames/users"
    headers = {"Content-Type": "application/json"}
    data = {"usernames": [username], "excludeBannedUsers": True}
    try:
        async with aiohttp.ClientSession() as session:
            async with session.post(url, json=data, headers=headers) as resp:
                res = await resp.json()
                if "data" in res and res["data"]:
                    return not res["data"][0].get("hasUser", True)
    except Exception as e:
        print("❌ API error:", e)
    return False

async def hunter_loop(update_callback=None, speed=BOT_SPEED):
    while True:
        username = generate_username()
        if username in checked_usernames:
            await asyncio.sleep(0)
            continue

        is_available = await check_username(username)
        checked_usernames.add(username)
        save_usernames()

        if update_callback:
            update_callback(username, is_available)

        await asyncio.sleep(1 / speed)
