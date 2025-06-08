import os
from flask import Flask, send_from_directory
from threading import Thread
from bot import run_bot  # ✅ Make sure your `bot.py` defines run_bot()

app = Flask(__name__, static_folder='static')

@app.route('/')
def index():
    return send_from_directory('static', 'index.html')

# ✅ Start bot in a background thread only if enabled
if os.getenv("RUN_BOT", "true").lower() == "true":
    Thread(target=run_bot).start()

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 10000))
    app.run(host='0.0.0.0', port=port)
