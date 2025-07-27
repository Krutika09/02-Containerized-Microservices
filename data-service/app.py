# data-service/app.py
from flask import Flask, jsonify
import redis
import requests

app = Flask(__name__)
cache = redis.Redis(host='redis', port=6379)

@app.route('/user/<name>', methods=['GET'])
def get_user(name):
    cached = cache.get(name)
    if cached:
        return jsonify({'cached': True, 'data': eval(cached)})

    response = requests.get('http://user-service:5000/users')
    users = response.json()
    for user in users:
        if user['name'].lower() == name.lower():
            cache.set(name, str(user))
            return jsonify({'cached': False, 'data': user})

    return jsonify({'message': 'User not found'}), 404

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)

