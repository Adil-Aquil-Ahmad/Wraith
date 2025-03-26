import base64

encrypted_message = "NAPVAbEY0TGwLVvHfVkWimNd3mW0+MyoPqmxEuMs4B0="

try:
    decoded = base64.b64decode(encrypted_message)
    print("Successfully decoded Base64!")
except Exception as e:
    print("Base64 Decoding Failed:", str(e))