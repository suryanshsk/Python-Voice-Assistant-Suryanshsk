from flask import Flask, request, jsonify
from pymongo import MongoClient
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity

app = Flask(__name__)

# Configuring JWT Secret Key
app.config['JWT_SECRET_KEY'] = 'supersecretkey'  # Use a strong key in production
jwt = JWTManager(app)

# MongoDB connection
client = MongoClient('mongodb://localhost:27017/')
db = client.virtual_assistant

# Route to register a new user
@app.route('/register', methods=['POST'])
def register():
    username = request.json.get('username')
    password = request.json.get('password')

    if not username or not password:
        return jsonify({"error": "Username and password required"}), 400

    if db.users.find_one({"username": username}):
        return jsonify({"error": "Username already exists"}), 400

    user = {
        "username": username,
        "password": password,
        "data": {
            "notes": [],
            "tasks": []
        }
    }
    db.users.insert_one(user)
    return jsonify({"message": "User registered successfully"}), 201

# Route to login and get JWT token
@app.route('/login', methods=['POST'])
def login():
    username = request.json.get('username')
    password = request.json.get('password')

    user = db.users.find_one({"username": username})

    if not user or user['password'] != password:
        return jsonify({"error": "Invalid username or password"}), 401

    # Create JWT token
    access_token = create_access_token(identity=username)
    return jsonify(access_token=access_token), 200

# Route to sync notes (multi-device sync)
@app.route('/sync/notes', methods=['POST'])
@jwt_required()
def sync_notes():
    username = get_jwt_identity()
    notes = request.json.get('notes')

    if not notes:
        return jsonify({"error": "No notes provided"}), 400

    # Update user's notes
    db.users.update_one({"username": username}, {"$set": {"data.notes": notes}})
    return jsonify({"message": "Notes synced successfully"}), 200

# Route to get synced notes
@app.route('/sync/notes', methods=['GET'])
@jwt_required()
def get_notes():
    username = get_jwt_identity()
    user = db.users.find_one({"username": username})

    if not user:
        return jsonify({"error": "User not found"}), 404

    notes = user.get('data', {}).get('notes', [])
    return jsonify({"notes": notes}), 200

# Route to sync tasks (multi-device sync)
@app.route('/sync/tasks', methods=['POST'])
@jwt_required()
def sync_tasks():
    username = get_jwt_identity()
    tasks = request.json.get('tasks')

    if not tasks:
        return jsonify({"error": "No tasks provided"}), 400

    # Update user's tasks
    db.users.update_one({"username": username}, {"$set": {"data.tasks": tasks}})
    return jsonify({"message": "Tasks synced successfully"}), 200

# Route to get synced tasks
@app.route('/sync/tasks', methods=['GET'])
@jwt_required()
def get_tasks():
    username = get_jwt_identity()
    user = db.users.find_one({"username": username})

    if not user:
        return jsonify({"error": "User not found"}), 404

    tasks = user.get('data', {}).get('tasks', [])
    return jsonify({"tasks": tasks}), 200

if __name__ == '__main__':
    app.run(debug=True)
