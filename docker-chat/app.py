from flask import Flask, render_template, request, jsonify
import random
import datetime
import os

app = Flask(__name__)

RESPONSES = {
    "tere": ["Tere!", "Tsau!", "Mis toimub?"],
    "kuidas": ["Hästi läheb!", "Olen container'is!", "Docker on praktiline!"],
    "kes": ["Olen chat bot", "Container bot", "Sinu Docker assistent"],
    "aeg": [f"Praegu on {datetime.datetime.now().strftime('%H:%M')}"],
    "info": ["Töötab Docker'is", "Python + Flask", "Port 5000"]
}

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/api/chat', methods=['POST'])
def chat():
    user_message = request.json.get('message', '').lower()
    
    response = "Ei saa aru... Proovi: tere, kuidas, kes, aeg, info"
    for keyword, replies in RESPONSES.items():
        if keyword in user_message:
            response = random.choice(replies)
            break
    
    return jsonify({
        'response': response,
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
    app.run(host='0.0.0.0', port=5000, debug=False)
'
