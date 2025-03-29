from Crypto.Cipher import AES
import base64
import os
import random

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
