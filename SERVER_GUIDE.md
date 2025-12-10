# Wraith - Anonymous Tor-based Social Platform

## Server Selection System

Wraith now supports three connection modes:

### Mode 1: Shared Server (1-999)
- Choose a server number between 1-999
- Each number has its own persistent onion address
- Multiple users can connect to the same server by using the same number
- If someone else is already running that server number, you'll automatically connect as a client
- Perfect for sharing with friends - just tell them your server number!

**Example:**
- Person A starts Wraith, chooses Mode 1, enters server number "42"
- Server 42 starts and gets its onion address
- Person B starts Wraith, chooses Mode 1, enters server number "42"
- Person B's browser automatically connects to Person A's running server
- Both can now chat, share posts, etc. on the same server!

### Mode 2: Private Wraithint Server
- Uses your personal persistent wraithint onion address
- Same address every time
- Private server just for you
- Original wraithint keys are never modified

### Mode 3: Random Anonymous Mode  
- Generates a new random onion address each session
- Maximum privacy and anonymity
- Address changes every time you run it
- Perfect for one-time anonymous sessions

## How It Works

**Shared Servers (Mode 1):**
- Each server number (1-999) has its own directory: `tor/servers/server_XXX/`
- When you start a server number, it checks if that port is already in use
- If running: Just launches browser to connect
- If not running: Starts full Tor + Flask server with that number's keys
- Each server runs on port 8000 + server_number (e.g., server 42 runs on port 8042)

**Private Server (Mode 2):**
- Uses `tor/hidden_service/` directory
- Your original wraithint keys stay safe here
- Runs on port 8000

**Random Server (Mode 3):**
- Uses `tor/temp_hidden_service/` directory  
- Deleted and recreated each session
- Runs on port 8000

## Quick Start

1. Run: `python app.py`
2. Choose mode (1, 2, or 3)
3. If Mode 1: Enter server number (1-999)
4. Wait for Tor to bootstrap
5. Browser opens automatically
6. Share your server number (Mode 1) or onion address with others!

## Connecting to Others

**To connect to someone's shared server:**
- Both choose Mode 1
- Both enter the SAME server number
- The second person will auto-connect to the first person's server

**To connect to someone's private/random server:**
- Open a new tab in the Wraith browser
- Enter their onion address in the URL bar
- Navigate to their server

