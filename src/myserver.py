import os
from flask import Flask, request, jsonify
from threading import Thread

app = Flask('')
app.json.ensure_ascii = False
bot_instance = None


@app.route('/')
def home():
    return "Server is running!"


@app.route('/api/guilds', methods=['GET'])
def get_guilds():
    # 1. Validate API Key
    api_key = os.environ.get('API_KEY')
    if not api_key:
        response = jsonify({"error": "Server error: API_KEY environment variable is not configured."})
        response.headers['Access-Control-Allow-Origin'] = '*'
        return response, 500

    auth_header = request.headers.get('Authorization')
    if not auth_header or not auth_header.startswith('Bearer '):
        response = jsonify({"error": "Unauthorized: Missing or invalid token format."})
        response.headers['Access-Control-Allow-Origin'] = '*'
        return response, 401

    provided_key = auth_header.split(' ')[1]
    if provided_key != api_key:
        response = jsonify({"error": "Unauthorized: Invalid API key."})
        response.headers['Access-Control-Allow-Origin'] = '*'
        return response, 401

    # 2. Check if bot is ready
    if not bot_instance or not bot_instance.is_ready():
        response = jsonify({"error": "Service Unavailable: Bot is not ready yet."})
        response.headers['Access-Control-Allow-Origin'] = '*'
        return response, 503

    # 3. Retrieve connected guilds
    guilds_data = []
    for guild in bot_instance.guilds:
        guilds_data.append({
            "id": str(guild.id),
            "name": guild.name,
            "member_count": guild.member_count,
            "icon_url": str(guild.icon.url) if guild.icon else None
        })

    response = jsonify({"guilds": guilds_data, "count": len(guilds_data)})
    response.headers['Access-Control-Allow-Origin'] = '*'
    response.headers['Access-Control-Allow-Headers'] = 'Authorization, Content-Type'
    response.headers['Access-Control-Allow-Methods'] = 'GET, OPTIONS'
    return response


@app.route('/api/guilds', methods=['OPTIONS'])
def handle_options():
    response = jsonify({"status": "ok"})
    response.headers['Access-Control-Allow-Origin'] = '*'
    response.headers['Access-Control-Allow-Headers'] = 'Authorization, Content-Type'
    response.headers['Access-Control-Allow-Methods'] = 'GET, OPTIONS'
    return response


def run():
    port = int(os.environ.get('PORT', 8080))
    app.run(host='0.0.0.0', port=port)


def server_on(bot):
    global bot_instance
    bot_instance = bot
    thread = Thread(target=run)
    thread.start()
