from Crypto.Cipher import AES
import base64
import os
import random

def generate_room_code():
    return str(random.randint(100000, 999999))

def pad_message(message):
    pad_size = 16 - (len(message) % 16)
    return message + chr(pad_size) * pad_size

def encrypt_message(message, key):
    iv = os.urandom(16)
    cipher = AES.new(key, AES.MODE_CBC, iv)
    padded = pad_message(message)
    encrypted_bytes = cipher.encrypt(padded.encode())
    encrypted_data = base64.b64encode(iv + encrypted_bytes).decode("utf-8")
    return encrypted_data
