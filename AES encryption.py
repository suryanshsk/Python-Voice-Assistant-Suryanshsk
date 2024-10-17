from flask import Flask, request, jsonify
from pymongo import MongoClient
from werkzeug.utils import secure_filename
from Crypto.Cipher import AES
import os

app = Flask(__name__)

# MongoDB connection
client = MongoClient('mongodb://localhost:27017/')
db = client.virtual_assistant

# AES encryption key (use a better key management in production)
SECRET_KEY = b'your_32_byte_key_here'

# Function to pad data to be AES block size compliant
def pad(data):
    return data + (AES.block_size - len(data) % AES.block_size) * chr(AES.block_size - len(data) % AES.block_size)

# Function to unpad data
def unpad(data):
    return data[:-ord(data[len(data) - 1:])]

# AES Encryption function
def encrypt_data(data):
    cipher = AES.new(SECRET_KEY, AES.MODE_ECB)
    return cipher.encrypt(pad(data).encode('utf-8')).hex()

# AES Decryption function
def decrypt_data(encrypted_data):
    cipher = AES.new(SECRET_KEY, AES.MODE_ECB)
    decrypted = cipher.decrypt(bytes.fromhex(encrypted_data)).decode('utf-8')
    return unpad(decrypted)

# Route to set opt-out for data collection
@app.route('/user/<username>/opt-out', methods=['POST'])
def opt_out(username):
    user = db.users.find_one({"username": username})
    if not user:
        return jsonify({"error": "User not found"}), 404

    db.users.update_one({"username": username}, {"$set": {"dataCollectionOptOut": True}})
    return jsonify({"message": "Opted out of data collection"})

# Route to upload and encrypt voice recording
@app.route('/user/<username>/upload', methods=['POST'])
def upload_recording(username):
    user = db.users.find_one({"username": username})
    if not user:
        return jsonify({"error": "User not found"}), 404

    if user.get('dataCollectionOptOut'):
        return jsonify({"error": "User has opted out of data collection"}), 403

    if 'voice' not in request.files:
        return jsonify({"error": "No voice file uploaded"}), 400

    file = request.files['voice']
    filename = secure_filename(file.filename)

    # Encrypt file content
    file_data = file.read()
    encrypted_recording = encrypt_data(file_data.decode('utf-8'))

    # Save encrypted data to the user
    db.users.update_one({"username": username}, {"$push": {"encryptedRecordings": encrypted_recording}})

    return jsonify({"message": "Voice recording uploaded and encrypted"})

# Route to delete a voice recording
@app.route('/user/<username>/recording/<int:index>', methods=['DELETE'])
def delete_recording(username, index):
    user = db.users.find_one({"username": username})
    if not user:
        return jsonify({"error": "User not found"}), 404

    encrypted_recordings = user.get('encryptedRecordings', [])
    if index < 0 or index >= len(encrypted_recordings):
        return jsonify({"error": "Recording not found"}), 404

    encrypted_recordings.pop(index)
    db.users.update_one({"username": username}, {"$set": {"encryptedRecordings": encrypted_recordings}})
    return jsonify({"message": "Voice recording deleted"})

# Route to get decrypted voice recording
@app.route('/user/<username>/recording/<int:index>', methods=['GET'])
def get_recording(username, index):
    user = db.users.find_one({"username": username})
    if not user:
        return jsonify({"error": "User not found"}), 404

    encrypted_recordings = user.get('encryptedRecordings', [])
    if index < 0 or index >= len(encrypted_recordings):
        return jsonify({"error": "Recording not found"}), 404

    decrypted_recording = decrypt_data(encrypted_recordings[index])
    return jsonify({"decryptedRecording": decrypted_recording})

# Route to create a user
@app.route('/user', methods=['POST'])
def create_user():
    username = request.json.get('username')
    if not username:
        return jsonify({"error": "Username is required"}), 400

    if db.users.find_one({"username": username}):
        return jsonify({"error": "Username already exists"}), 400

    user = {
        "username": username,
        "dataCollectionOptOut": False,
        "encryptedRecordings": []
    }
    db.users.insert_one(user)
    return jsonify({"message": "User created"}), 201

if __name__ == '__main__':
    app.run(debug=True)
