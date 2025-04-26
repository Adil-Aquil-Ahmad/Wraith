# Wraith: An Encrypted and Anonymous Tor-Based Messaging Platform

Description
Wraith is a privacy-focused, AI-inspired messaging platform that operates securely over the Tor network. It is designed to deliver fully anonymous, end-to-end encrypted communications resistant to surveillance and metadata attacks.

Built using a PyQt5-based client interface and Tor as its network layer, Wraith currently uses AES encryption combined with Base64 encoding to secure messages. The next generation of Wraith focuses on improving security, eliminating vulnerabilities like server-side key storage, and transitioning toward a decentralized architecture.

Key Features
Advanced Encryption and Security:

End-to-End Encryption (E2EE): Full encryption of messages, ensuring only sender and receiver can read them.

Ephemeral Keys: Session-based encryption keys to reduce risks from prolonged key exposure.

No Server-Side Key Storage: Keys exist only temporarily on user devices.

Architectural Enhancements:

Decentralized or Relay-Based Communication: Moves beyond the traditional client-server model for enhanced anonymity.

Metadata Minimization: Structures communication and storage to resist correlation and traffic analysis attacks.

Encrypted Local Storage: Optional encrypted storage of session logs if required.

User Interface and User Experience:

PyQt5-Based Browser Interface: Modern, lightweight, and privacy-centric design.

Seamless Tor Configuration: Automatic setup of Tor networking for ease of use.

Multi-Chatroom Support: Enables multiple secure chat sessions simultaneously.

Anonymous User Authentication: Use of Tor-based credentials or Onion addresses for login.

Use Cases
Private Communication:

Anonymous messaging for activists, journalists, or privacy-focused individuals.

Secure Collaboration:

Teams needing high-trust, high-security private communication channels.

Privacy-Conscious Communities:

Secure chatrooms for communities valuing digital rights, freedom of speech, and anonymity.

Technical Explanation
Encryption System:
Messages are secured using AES encryption with Base64 encoding. During improvements, secure key exchange mechanisms such as RSA and ephemeral keys will be integrated to remove current vulnerabilities.

Network Architecture:
Initially client-server based, Wraith is being transitioned toward a decentralized (or relay-based) system using onion routing principles from Tor to maximize anonymity.

Database and Storage:
The new version limits database use to encrypted local storage if absolutely necessary. Session logs, if stored, will be encrypted using symmetric encryption techniques.

User Experience:
Built with PyQt5 and PyQtWebEngine, Wraith offers a clean, simple interface that automatically configures Tor and handles secure onboarding, enabling users to focus on private communication without technical barriers.

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
(https://youtu.be/L5L7oO9yimM

Technology & Languages
Python

PyQt5 & PyQtWebEngine – GUI framework for a browser-based chat client.

PyCryptodome – AES encryption for message security.

Feedparser – Parses RSS/Atom feeds for potential dark web monitoring.

Requests – Handles HTTP requests within the Tor network.

BeautifulSoup4 – Extracts and processes HTML data securely.

Flask – Lightweight web framework for handling chat requests.

Flask-SocketIO – Enables real-time, bidirectional communication.

Werkzeug – Secure WSGI toolkit for handling authentication.

Gevent & Gevent-WebSocket – Optimizes WebSocket performance.

Tor APIs

MongoDB

# How to Use

Step - 1

Unzip the tor folder in the current folder

Edit the torrc file in the tor folder:

DataDirectory C:\Users\ADIL\Documents\GitHub\Wraith\tor\
HiddenServiceDir C:\Users\ADIL\Documents\GitHub\Wraith\tor\hidden_service

update these according to your current folder path 

Step - 2

Run this Command in your CMD "'folder location'\Wraith\tor\tor.exe -f 'folder location'\Wraith\tor\torrc"

for eg: C:\Users\ADIL\Documents\GitHub\Wraith\tor\tor.exe -f C:\Users\ADIL\Documents\GitHub\Wraith\tor\torrc

Step - 3

Run python app.py in your terminal

Step - 4

Run python browser.py in another terminal

The app should run Successfully if you followed all the steps

For creating a new executable use:
pyinstaller --name WraithApp --onefile --windowed app.py
pyinstaller WraithApp.spec

