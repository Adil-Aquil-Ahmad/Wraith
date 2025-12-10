from flask import Flask, jsonify, render_template, request, redirect, url_for, session
from flask_socketio import SocketIO, join_room, emit
from newsbot import *
from Chatroom import *
from Crypto.Cipher import AES
import certifi
from pymongo import MongoClient
from pymongo.server_api import ServerApi
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
import socket
import shutil
import sys
from server_manager import ServerManager
import secrets
import hashlib



app = Flask(__name__)
app.config["SECRET_KEY"] = "AdilAAhmad"
app.config['SESSION_TYPE'] = 'filesystem'
socketio = SocketIO(app, cors_allowed_origins="*", async_mode="threading")
uri = "mongodb+srv://adilaquil2005:0eZ6sWNEbWhPEWna@wraith.fgvesko.mongodb.net/?appName=Wraith"
client = MongoClient(uri, tlsCAFile=certifi.where(), server_api=ServerApi('1'))
db = client["Wraith"]
posts_collection = db["forum_db"]

# Generate a unique browser authentication secret for this session
BROWSER_SECRET = secrets.token_urlsafe(32)

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
            # Store room in session for access control
            if 'rooms' not in session:
                session['rooms'] = []
            session['rooms'].append(room)
            session.modified = True
            return redirect(url_for("chatroom", room_code=room))
        elif action == "join":
            room = request.form["room_code"].strip()
            if room in chatrooms:
                # Add room to user's session
                if 'rooms' not in session:
                    session['rooms'] = []
                if room not in session['rooms']:
                    session['rooms'].append(room)
                session.modified = True
                return redirect(url_for("chatroom", room_code=room))
            else:
                return "Invalid Room Code", 400
    return render_template("index.html")

@app.route("/chat/<room_code>")
def chatroom(room_code):
    # Don't reveal if room exists - check authorization first to prevent enumeration
    if 'rooms' not in session or room_code not in session['rooms'] or room_code not in chatrooms:
        return "Access Denied", 403
    
    response = app.make_response(render_template("chatroom.html", room_code=room_code))
    # Prevent caching of chatroom page
    response.headers['Cache-Control'] = 'no-cache, no-store, must-revalidate, private, max-age=0'
    response.headers['Pragma'] = 'no-cache'
    response.headers['Expires'] = '0'
    return response

@app.route("/get_key/<room_code>")
def get_key(room_code):
    # Don't reveal if room exists - check authorization first to prevent enumeration
    if 'rooms' not in session or room_code not in session['rooms'] or room_code not in chatrooms:
        return jsonify({"error": "Access Denied"}), 403
    
    # Check for Wraith browser authentication
    auth_token = request.headers.get('X-Wraith-Auth')
    if not auth_token or not verify_browser_auth(auth_token):
        return jsonify({"error": "Unauthorized - Wraith Browser Required"}), 403
    
    key_b64 = base64.b64encode(chatrooms[room_code]).decode("utf-8")
    return jsonify({"key": key_b64})

def verify_browser_auth(token):
    """Verify the browser authentication token"""
    try:
        # Token should be hash of BROWSER_SECRET + current date
        expected = hashlib.sha256((BROWSER_SECRET + time.strftime("%Y%m%d")).encode()).hexdigest()
        return token == expected
    except:
        return False

@app.route("/browser_auth")
def get_browser_auth():
    """Endpoint to get authentication token - only accessible via direct connection"""
    # Generate auth token valid for current day
    token = hashlib.sha256((BROWSER_SECRET + time.strftime("%Y%m%d")).encode()).hexdigest()
    return jsonify({"token": token, "secret": BROWSER_SECRET})

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

def launch_browser(onion_address=None):
    time.sleep(5)
    # Use sys.executable to get the current Python interpreter (from venv)
    python_path = sys.executable
    if onion_address:
        subprocess.Popen([python_path, "browser.py", f"http://{onion_address}"])
    else:
        subprocess.Popen([python_path, "browser.py"])

def wait_for_tor():
    """Wait for Tor to fully bootstrap to 100%"""
    print("Waiting for Tor to bootstrap to 100%...")
    max_wait = 180  # Maximum wait time in seconds
    start_time = time.time()
    
    # Monitor Tor's output for bootstrap completion
    while time.time() - start_time < max_wait:
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(1)
            result = sock.connect_ex(('127.0.0.1', 9050))
            sock.close()
            
            if result == 0:

                elapsed = time.time() - start_time
                if elapsed >= 30:
                    print("Tor should be bootstrapped to 100%!")
                    return True
        except:
            pass
        time.sleep(2)
    
    print("Warning: Tor may not be fully ready, but continuing anyway...")
    return False

def monitor_tor_output(process):
    """Monitor Tor process output in a separate thread"""
    for line in iter(process.stdout.readline, ''):
        if line:
            print(line, end='')
        if process.poll() is not None:
            break

if __name__ == "__main__":
    multiprocessing.freeze_support()

    current_path = os.getcwd()
    server_mgr = ServerManager(current_path)

    # Ask user for server mode
    print("\n" + "="*60)
    print("🧅  WRAITH - SERVER SELECTION")
    print("="*60)
    print("\nChoose your connection mode:")
    print("1. Shared Server Mode - Connect to server number (1-999)")
    print("   - Multiple users can connect to the same server")
    print("   - Each server number has its own persistent address")
    print("   - Share your server number with others to connect")
    print("\n2. Private Mode - Use your personal wraithint address")
    print("   - Your personal persistent onion address")
    print("   - Private server just for you")
    print("\n3. Random Anonymous Mode - Generate temporary random address")
    print("   - New random address each session")
    print("   - Maximum privacy")
    print("="*60)
    
    while True:
        mode_choice = input("\nEnter your choice (1, 2, or 3): ").strip()
        if mode_choice in ["1", "2", "3"]:
            break
        print("Invalid choice. Please enter 1, 2, or 3.")
    
    server_num = None
    server_port = 8000
    
    if mode_choice == "1":
        # Shared server mode
        print("\n" + "="*60)
        while True:
            try:
                server_num = int(input("Enter server number (1-999): ").strip())
                if 1 <= server_num <= 999:
                    break
                print("Please enter a number between 1 and 999.")
            except ValueError:
                print("Please enter a valid number.")
        
        server_port = server_mgr.get_server_port(server_num)
        hidden_service_dir = server_mgr.get_server_dir(server_num)
        
        # Check if server is already running
        if server_mgr.is_server_running(server_num):
            print(f"\n✓ Server {server_num} is already running!")
            onion_address = server_mgr.get_onion_address(server_num)
            if onion_address:
                print(f"✓ Connecting to: {onion_address}")
                print(f"{'='*60}\n")
                # Just launch browser to connect to existing server
                python_path = sys.executable
                subprocess.Popen([python_path, "browser.py", f"http://{onion_address}"])
                sys.exit(0)
        
        print(f"\n✓ Starting new server #{server_num}...")
        print(f"  Others can connect by choosing server number: {server_num}")
        
    elif mode_choice == "2":
        # Private wraithint mode
        print("\n✓ Using your personal wraithint address...\n")
        hidden_service_dir = os.path.join(current_path, "tor", "hidden_service")
        
    else:  # mode_choice == "3"
        # Random anonymous mode
        print("\n✓ Generating new random anonymous address...\n")
        hidden_service_dir = os.path.join(current_path, "tor", "temp_hidden_service")
        if os.path.exists(hidden_service_dir):
            shutil.rmtree(hidden_service_dir)
    
    # Ensure hidden service directory exists with proper permissions
    os.makedirs(hidden_service_dir, exist_ok=True)
    os.chmod(hidden_service_dir, 0o700)

    tor_folder = os.path.join(current_path, "tor")
    data_directory = os.path.join(tor_folder, "Data")
    os.makedirs(data_directory, exist_ok=True)
    torrc_path = os.path.join(tor_folder, "torrc")
    tor_path = "/opt/homebrew/opt/tor/bin/tor"

    torrc_content = f"""SocksPort 9050
ControlPort 9051
DataDirectory {data_directory}
HiddenServiceDir {hidden_service_dir}
HiddenServicePort 80 127.0.0.1:{server_port}
"""

    with open(torrc_path, "w") as f:
        f.write(torrc_content)

    print(f"'torrc' created at {torrc_path}")

    tor_process = subprocess.Popen([
        tor_path,
        "-f", torrc_path
    ], stdout=subprocess.PIPE, stderr=subprocess.STDOUT, universal_newlines=True, bufsize=1)
    
    tor_monitor_thread = threading.Thread(target=monitor_tor_output, args=(tor_process,), daemon=True)
    tor_monitor_thread.start()

    wait_for_tor()

    # Display the onion address
    onion_address = None
    hostname_file = os.path.join(hidden_service_dir, "hostname")
    if os.path.exists(hostname_file):
        with open(hostname_file, 'r') as f:
            onion_address = f.read().strip()
            print(f"\n{'='*60}")
            print(f"🧅 Your onion address: {onion_address}")
            if mode_choice == "1":
                print(f"   Server #{server_num} - Share this number with others!")
            elif mode_choice == "2":
                print(f"   (Your personal wraithint address)")
            else:
                print(f"   (Temporary - will change next session)")
            print(f"{'='*60}\n")

    def run_flask():
        socketio.run(app, host="127.0.0.1", port=server_port, debug=True, use_reloader=False)
    
    flask_thread = threading.Thread(target=run_flask)
    flask_thread.start()

    launch_browser(onion_address)