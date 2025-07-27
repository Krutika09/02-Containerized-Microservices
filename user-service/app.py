from flask import Flask, request, jsonify
import psycopg2

app = Flask(__name__)

def get_db_connection():
    conn = psycopg2.connect(
        host='postgres',
        database='users',
        user='postgres',
        password='postgres'
    )
    return conn

@app.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    name = data.get('name')
    email = data.get('email')

    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("INSERT INTO users (name, email) VALUES (%s, %s)", (name, email))
    conn.commit()
    cur.close()
    conn.close()

    return jsonify({"message": "User registered successfully"})

@app.route('/users', methods=['GET'])
def get_all_users():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("SELECT name, email FROM users")
    rows = cur.fetchall()
    cur.close()
    conn.close()

    users = [{"name": row[0], "email": row[1]} for row in rows]
    return jsonify(users)

@app.route('/delete/<name>', methods=['DELETE'])
def delete_user(name):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("DELETE FROM users WHERE name = %s", (name,))
    conn.commit()
    cur.close()
    conn.close()
    return jsonify({"message": f"User {name} deleted successfully"})


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)

