from flask import Flask, jsonify, render_template, request, redirect, url_for
from flask_socketio import SocketIO, join_room, emit
from newsbot import *
from Chatroom import *
from Crypto.Cipher import AES
from pymongo import MongoClient
import base64
import os
import random
from werkzeug.utils import secure_filename
from bson import ObjectId
from bson import Binary
import threading
import subprocess
import time
import multiprocessing



app = Flask(__name__)
app.config["SECRET_KEY"] = "AdilAAhmad"
socketio = SocketIO(app, cors_allowed_origins="*", async_mode="threading")
client = MongoClient("mongodb://localhost:27017/")
db = client["forum_db"]
posts_collection = db["posts"]

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

@socketio.on("join")
def handle_join(data):
    room = data["room_code"]
    username = data["username"]
    join_room(room)
    emit("message", {"username": "System", "message": f"{username} has joined the chat!", "msg_id": "system_"+str(random.randint(1000,9999))}, room=room)

@socketio.on("message")
def handle_message(data):
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
    room = data["room_code"]
    msg_id = data["msg_id"]
    emit("delete_message", {"msg_id": msg_id}, room=room)

@app.route("/chat", methods=["GET", "POST"])
def chat_home():
    if request.method == "POST":
        action = request.form["action"]
        if action == "create":
            room = generate_room_code()
            chatrooms[room] = os.urandom(16)
            return redirect(url_for("chatroom", room_code=room))
        elif action == "join":
            room = request.form["room_code"].strip()
            if room in chatrooms:
                return redirect(url_for("chatroom", room_code=room))
            else:
                return "Invalid Room Code", 400
    return render_template("index.html")

@app.route("/chat/<room_code>")
def chatroom(room_code):
    if room_code not in chatrooms:
        return "Invalid Room Code", 400
    return render_template("chatroom.html", room_code=room_code)

@app.route("/get_key/<room_code>")
def get_key(room_code):
    if room_code not in chatrooms:
        return jsonify({"error": "Invalid Room Code"}), 400
    key_b64 = base64.b64encode(chatrooms[room_code]).decode("utf-8")
    return jsonify({"key": key_b64})

# Forum Routes
@app.route("/forum")
def forum():
    posts = list(posts_collection.find({}))
    
    for post in posts:
        post["_id"] = str(post["_id"])
        if post["image"]:
            post["image"] = base64.b64encode(post["image"]).decode("utf-8")

    return render_template("forum.html", posts=posts)

@app.route("/submit_post", methods=["POST"])
def submit_post():
    title = request.form.get("title", "").strip()
    content = request.form.get("content", "").strip()
    image = request.files.get("image")

    if not title or not content:
        return "Title and Content are required", 400

    post_data = {"title": title, "content": content, "image": None, "comments": []}

    if image:
        image_data = image.read()
        post_data["image"] = Binary(image_data)

    post_id = posts_collection.insert_one(post_data).inserted_id
    return redirect(url_for("post_view", post_id=str(post_id)))

@app.route("/post/<string:post_id>")
def post_view(post_id):
    try:
        post = posts_collection.find_one({'_id': ObjectId(post_id)})
        if not post:
            return "Post not found", 404

        post["_id"] = str(post["_id"])

        if post["image"]:
            post["image"] = base64.b64encode(post["image"]).decode("utf-8")

        return render_template("post.html", post=post)
    except Exception:
        return "Invalid Post ID", 400

@app.route("/post/<string:post_id>/comment", methods=["POST"])
def add_comment(post_id):
    comment_text = request.form.get("comment", "").strip()
    if not comment_text:
        return "Comment cannot be empty", 400

    try:
        posts_collection.update_one(
            {"_id": ObjectId(post_id)}, 
            {"$push": {"comments": {"user": "Anonymous", "text": comment_text}}}
        )
        return redirect(url_for("post_view", post_id=post_id))
    except Exception:
        return "Invalid Post ID", 400

def run_flask():
    socketio.run(app, host="127.0.0.1", port=8000, debug=True, use_reloader=False)

def launch_browser():
    time.sleep(5)
    subprocess.Popen(["python", "browser.py"])

if __name__ == "__main__":
    multiprocessing.freeze_support()

    tor_process = subprocess.Popen([
        r"C:\Users\ADIL\Documents\GitHub\Wraith\tor\tor.exe",
        "-f", r"C:\Users\ADIL\Documents\GitHub\Wraith\tor\torrc"
    ])

    time.sleep(15)

    flask_thread = threading.Thread(target=run_flask)
    flask_thread.start()

    launch_browser()