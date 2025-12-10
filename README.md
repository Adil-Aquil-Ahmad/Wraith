# Wraith: An Encrypted and Anonymous Tor-Based Messaging Platform

Description
Wraith is a privacy-focused, AI-inspired messaging platform that operates securely over the Tor network. It is designed to deliver fully anonymous, end-to-end encrypted communications resistant to surveillance and metadata attacks.

Built using a PyQt6-based client interface and Tor as its network layer, Wraith uses AES-128-CBC encryption to secure messages. The platform emphasizes security hardening with multiple layers of protection against information leakage, memory forensics, and unauthorized access.

Key Features
Advanced Encryption and Security:

End-to-End Encryption (E2EE): AES-128-CBC encryption of messages, ensuring only authorized users can read them.

Session-Based Access Control: Flask sessions track authorized chatrooms, preventing unauthorized access even with direct URLs.

Memory Protection: Decrypted messages are immediately overwritten in memory with random data, then nullified to prevent memory forensics.

Browser Hardening: DevTools detection alerts users to potential inspection, cache prevention headers, disabled context menus.

Console Logging Elimination: All sensitive data logging removed from browser console to prevent message exposure.

Room Enumeration Prevention: Identical error responses prevent attackers from discovering which chatrooms exist on a server.

Server Selection Modes:

Shared Servers (1-999): Choose from 999 pre-numbered servers for community-based anonymous communication.

Private Server (wraithint): Use the original persistent onion address for private, long-term chatrooms.

Random Anonymous Server: Generate temporary onion addresses for maximum anonymity with ephemeral communication.

Architectural Enhancements:

Multi-Mode Tor Hidden Services: Three distinct operational modes balancing persistence and anonymity.

Port-Based Server Management: Automatic port checking prevents duplicate server instances.

Session-Based Authorization: Users must explicitly join chatrooms through the interface, preventing URL-based attacks.

User Interface and User Experience:

PyQt6-Based Browser Interface: Modern, lightweight, privacy-centric design with built-in Tor SOCKS5 proxy.

Automatic Tor Bootstrap: 75-second wait ensures full Tor network connection before launching.

Multi-Chatroom Support: Secure multiple encrypted chat sessions simultaneously with per-room encryption keys.

Server Selection Menu: Interactive mode selection at startup with clear anonymity trade-offs.

Use Cases
Private Communication:

Anonymous messaging for activists, journalists, or privacy-focused individuals.

Secure Collaboration:

Teams needing high-trust, high-security private communication channels.

Privacy-Conscious Communities:

Secure chatrooms for communities valuing digital rights, freedom of speech, and anonymity.

Technical Explanation
Encryption System:
Messages are secured using AES-128-CBC encryption with 16-byte per-room keys. Decryption happens client-side in the browser using forge.js, ensuring server never handles plaintext. Keys are transmitted only to authorized sessions via the /get_key endpoint with browser authentication tokens.

Network Architecture:
Wraith operates as a Flask + SocketIO server behind Tor hidden services. Three operational modes provide flexibility:
- **Shared Servers (1-999)**: Each numbered server runs on port 8000+N with dedicated hidden service directory at tor/servers/server_XXX/
- **Private Server (wraithint)**: Original persistent onion address stored in tor/hidden_service/ for long-term private communication
- **Random Server**: Temporary hidden service generated at tor/temp_hidden_service/, deleted after use for maximum anonymity

Security Hardening:
Multiple layers protect against information leakage:
- **Memory Protection**: Decrypted messages overwritten with 'X'.repeat() then nullified, intermediate decryption variables cleared
- **Console Protection**: All console.log() statements removed, console.clear() after message deletion
- **Cache Prevention**: HTTP headers (Cache-Control, Pragma, Expires) and meta tags prevent browser caching
- **DevTools Detection**: Monitors window size differences every 500ms to detect inspection attempts
- **Session Authorization**: Flask sessions track authorized rooms, preventing direct URL manipulation
- **Enumeration Prevention**: Identical 403 errors whether room exists or not, preventing chatroom discovery
- **Context Menu Disabled**: Right-click disabled to prevent easy DOM inspection

Database and Storage:
MongoDB stores encrypted messages with room_code indexing. Session data stored in filesystem sessions. Tor hidden service keys persist in dedicated directories based on server mode selection.

User Experience:
PyQt6 browser automatically configures SOCKS5 proxy (127.0.0.1:9050) and accepts onion URLs via command-line arguments. The application handles full Tor bootstrap verification, launches browser with correct Python virtual environment, and provides clear server selection interface.

Workflow Diagram
https://imgur.com/a/G700nKT

Conclusion
Wraith aims to redefine private communication by offering a fully decentralized, encrypted messaging platform over Tor. By addressing existing vulnerabilities and adding advanced cryptographic practices, Wraith will empower users with true anonymity and security, ensuring their communications stay safe from surveillance and censorship.

Project Team
Lead Developer: Adil Aquil Ahmad
Responsible for the overall design, development, and implementation of the Wraith project.

Special Acknowledgment:
Prabhdeep Singh – Recognized for his valuable contributions through pull requests aimed at enhancing and refining the frontend user experience.

GitHub: https://github.com/Adil-Aquil-Ahmad/

Project Video
https://youtu.be/L5L7oO9yimM

Technology & Languages
Python

PyQt6 & PyQt6-WebEngine – GUI framework for Tor-enabled browser client.

PyCryptodome – AES-128-CBC encryption for message security.

Feedparser – Parses RSS/Atom feeds for dark web news monitoring.

Requests – Handles HTTP requests within the Tor network.

BeautifulSoup4 – Extracts and processes HTML data securely.

Flask – Lightweight web framework for handling chat requests with session management.

Flask-SocketIO – Enables real-time, bidirectional encrypted communication.

Werkzeug – Secure WSGI toolkit for handling authentication.

Gevent & Gevent-WebSocket – Optimizes WebSocket performance.

Forge.js – Client-side AES-CBC decryption in browser.

Tor Hidden Services – Provides anonymous .onion addresses for server hosting.

MongoDB – Encrypted message storage with room-based indexing.

# How to Use (macOS)

**Prerequisites:**
- macOS (tested on Apple Silicon)
- Homebrew installed
- Python 3.12+ with virtual environment
- MongoDB running locally

**Step 1 - Install Tor via Homebrew**

```bash
brew install tor
```

Tor will be installed at `/opt/homebrew/opt/tor/bin/tor` on Apple Silicon Macs.

**Step 2 - Configure Python Environment**

```bash
cd /path/to/Wraith
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

**Step 3 - Run Wraith**

```bash
python app.py
```

You'll be presented with three server modes:

**Mode 1 - Shared Server (1-999)**
- Enter a number between 1-999
- Each number represents a dedicated server with unique onion address
- Server runs on port 8000+N (e.g., server 42 uses port 8042)
- Hidden service keys stored in `tor/servers/server_XXX/`
- Ideal for semi-persistent community chatrooms

**Mode 2 - Private Server (wraithint)**
- Uses original persistent onion address
- Hidden service keys in `tor/hidden_service/`
- Runs on port 8000
- Best for long-term private communication

**Mode 3 - Random Anonymous Server**
- Generates temporary onion address
- Hidden service created at `tor/temp_hidden_service/`
- Maximum anonymity, deleted after use
- Perfect for ephemeral conversations

The application will:
1. Start Tor daemon and wait for 100% bootstrap
2. Launch PyQt6 browser with your onion address
3. Display the .onion URL in terminal

**Step 4 - Access Chatrooms**

- Create or join chatrooms via the web interface
- Share the onion URL with others (Tor Browser required for them)
- All messages encrypted with AES-128-CBC
- Session-based access prevents unauthorized room entry

**Security Features Active:**
✓ Console logging disabled (no decrypted messages in DevTools)
✓ Memory wiping after message decryption
✓ DevTools detection alerts
✓ Cache prevention headers
✓ Session-based room authorization
✓ Chatroom enumeration prevention
✓ Browser authentication tokens

**For creating a new executable:**
```bash
pyinstaller --name WraithApp --onefile --windowed app.py
```

