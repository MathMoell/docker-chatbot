from flask import Flask, render_template, request, jsonify
import random
import datetime
import os
import redis
import socket

app = Flask(__name__)

try:
    cache = redis.Redis(host='redis', port=6379, db=0)
    cache.ping()
    print("✅ Connected to Redis")
except redis.ConnectionError:
    cache = None
    print("⚠️ Redis connection failed")

RESPONSES = {
    "tere": ["Tere!", "Tsau!", "Mis toimub?"],
    "kuidas": ["Hästi läheb!", "Olen container'is!", "Docker on praktiline!"],
    "kes": ["Olen chat bot", "Container bot", "Sinu Docker assistent"],
    "aeg": [f"Praegu on {datetime.datetime.now().strftime('%H:%M')}"],
    "info": ["Töötab Docker'is", "Python + Flask", "Port 5000"]
}

@app.route('/health')
def health():
    redis_status = "connected" if cache and cache.ping() else "disconnected"
    return jsonify({
        "status": "OK",
        "redis": redis_status,
        "time": datetime.datetime.now().isoformat(),
        "container": socket.gethostname()
    })

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/api/chat', methods=['POST'])
def chat():
    user_message = request.json.get('message', '').lower()
    cache_key = f"chat:{user_message}"

    if cache:
        cached_response = cache.get(cache_key)
        if cached_response:
            print(f"💾 Cache HIT for '{user_message}'")
            return jsonify({
                'response': cached_response.decode('utf-8'),
                'cached': True,
                'timestamp': datetime.datetime.now().isoformat(),
                'container_id': os.environ.get('HOSTNAME', 'unknown')
            })
        else:
            print(f"🧠 Cache MISS for '{user_message}'")

    response = "Ei saa aru... Proovi: tere, kuidas, kes, aeg, info"
    for keyword, replies in RESPONSES.items():
        if keyword in user_message:
            response = random.choice(replies)
            break

    if cache:
        cache.setex(cache_key, 60, response)

    return jsonify({
        'response': response,
        'cached': False,
        'timestamp': datetime.datetime.now().isoformat(),
        'container_id': os.environ.get('HOSTNAME', 'unknown')
    })

@app.route('/api/stats')
def stats():
    return jsonify({
        'uptime': 'Docker container töötab',
        'python_version': '3.11',
        'framework': 'Flask',
        'container_id': os.environ.get('HOSTNAME', 'unknown')
    })

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
