from flask import Flask, send_from_directory
import os
import bot  # This will start your bot in background if RUN_BOT env var is set to true

app = Flask(__name__, static_folder='static')

@app.route('/')
def index():
    return send_from_directory('static', 'index.html')

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 10000))
    app.run(host='0.0.0.0', port=port)
