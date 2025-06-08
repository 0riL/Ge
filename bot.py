import time
import requests
import json
import os
from config import BOT_SPEED, LOG_FILE
from utils.github_sync import auto_push_to_github

def check_username_availability(username):
    try:
        response = requests.get(f'https://api.roblox.com/users/get-by-username?username={username}')
        if response.status_code == 200:
            data = response.json()
            return data.get('Id') is None
        return False
    except Exception as e:
        log_error(str(e))
        return False

def log_username(username):
    with open(LOG_FILE, 'a') as f:
        f.write(username + '\n')
    auto_push_to_github(LOG_FILE)

def log_error(error_message):
    with open('error_log.txt', 'a') as f:
        f.write(f'{time.ctime()}: {error_message}\n')

def run_bot():
    checked = set()
    if os.path.exists(LOG_FILE):
        with open(LOG_FILE, 'r') as f:
            checked = set(line.strip() for line in f)

    while True:
        username = generate_random_username()
        if username in checked:
            continue
        if check_username_availability(username):
            print(f'[AVAILABLE] {username}')
            log_username(username)
        else:
            print(f'[TAKEN] {username}')
        checked.add(username)
        time.sleep(1 / BOT_SPEED)

def generate_random_username():
    import random, string
    return ''.join(random.choices(string.ascii_lowercase + string.digits, k=4))

# Optional auto-run
if os.getenv("RUN_BOT", "true").lower() == "true":
    run_bot()
