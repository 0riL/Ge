from flask import Flask, send_from_directory, jsonify
from flask_socketio import SocketIO
import threading
import asyncio
import bot

app = Flask(__name__, static_folder='static')
socketio = SocketIO(app, cors_allowed_origins="*")

def send_update(username, available):
    socketio.emit('update', {'username': username, 'available': available})

def run_bot():
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop.run_until_complete(bot.hunter_loop(update_callback=send_update))

threading.Thread(target=run_bot, daemon=True).start()

@app.route('/')
def index():
    return send_from_directory('static', 'index.html')

@app.route('/checked')
def checked():
    return jsonify(list(bot.checked_usernames))

if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0', port=5000)
