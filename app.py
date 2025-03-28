from flask import Flask, jsonify, render_template, request, redirect, url_for
from flask_socketio import SocketIO, join_room, emit
from newsbot import *
from Crypto.Cipher import AES
import base64
import os
import random

app = Flask(__name__)
app.config["SECRET_KEY"] = "AdilAAhmad"
socketio = SocketIO(app, cors_allowed_origins="*")

# News Routes
@app.route('/')
def home():
    return render_template('news.html')

@app.route("/data/europe")
def europe_news():
    return jsonify(fetch_nytimes_europe())

@app.route("/data/all")
def all_news():
    return jsonify(fetch_all_nytimes_news())

@app.route("/data/africa")
def africa_news():
    return jsonify(fetch_nytimes_africa())

@app.route("/data/americas")
def americas_news():
    return jsonify(fetch_nytimes_americas())

@app.route("/data/asiapac")
def asiapac_news():
    return jsonify(fetch_nytimes_asiapac())

@app.route("/data/middleeast")
def middleeast_news():
    return jsonify(fetch_nytimes_middleast())

# Chatroom Routes
chatrooms = {}

def generate_room_code():
    """Generates a 6-digit random room code."""
    return str(random.randint(100000, 999999))

def pad_message(message):
    """Pad the message using PKCS7 padding to a multiple of 16 bytes."""
    pad_size = 16 - (len(message) % 16)
    return message + chr(pad_size) * pad_size

def encrypt_message(message, key):
    """Encrypt a message using AES-CBC mode (AES-128) and return Base64(iv+ciphertext)."""
    iv = os.urandom(16)
    cipher = AES.new(key, AES.MODE_CBC, iv)
    padded = pad_message(message)
    encrypted_bytes = cipher.encrypt(padded.encode())
    encrypted_data = base64.b64encode(iv + encrypted_bytes).decode("utf-8")
    return encrypted_data

@socketio.on("join")
def handle_join(data):
    """Handles users joining the chatroom."""
    room = data["room_code"]
    username = data["username"]
    join_room(room)
    emit("message", {"username": "System", "message": f"{username} has joined the chat!", "msg_id": "system_"+str(random.randint(1000,9999))}, room=room)

@socketio.on("message")
def handle_message(data):
    """Encrypts and broadcasts a message to all clients in the room."""
    room = data["room_code"]
    username = data["username"]
    message = data["message"]
    msg_id = data.get("msg_id")
    if room not in chatrooms:
        return
    key = chatrooms[room]
    encrypted_message = encrypt_message(message, key)
    emit("message", {"username": username, "message": encrypted_message, "msg_id": msg_id}, room=room)

@socketio.on("delete_message")
def handle_delete_message(data):
    """Broadcast deletion of a message (by msg_id) to all clients."""
    room = data["room_code"]
    msg_id = data["msg_id"]
    emit("delete_message", {"msg_id": msg_id}, room=room)

@app.route("/chat", methods=["GET", "POST"])
def chat_home():
    """Homepage where users create or join a chatroom."""
    if request.method == "POST":
        action = request.form["action"]
        if action == "create":
            room = generate_room_code()
            chatrooms[room] = os.urandom(16)
            return redirect(url_for("chatroom", room_code=room))
        elif action == "join":
            room = request.form["room_code"]
            if room in chatrooms:
                return redirect(url_for("chatroom", room_code=room))
            else:
                return "Invalid Room Code", 400
    return render_template("index.html")

@app.route("/chat/<room_code>")
def chatroom(room_code):
    """Chatroom page."""
    if room_code not in chatrooms:
        return "Invalid Room Code", 400
    return render_template("chatroom.html", room_code=room_code)

@app.route("/get_key/<room_code>")
def get_key(room_code):
    """Send AES key (Base64-encoded) securely to the client."""
    if room_code not in chatrooms:
        return jsonify({"error": "Invalid Room Code"}), 400
    key_b64 = base64.b64encode(chatrooms[room_code]).decode("utf-8")
    return jsonify({"key": key_b64})

if __name__ == "__main__":
    socketio.run(app, host="127.0.0.1", port=8000, debug=True)
