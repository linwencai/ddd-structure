from ast import parse
import base64
from cryptography.fernet import Fernet

def encrypt(text : str, key : str):

    key_bytes = generate_key(key).encode()
    text_bytes = text.encode()

    cipher = Fernet(key_bytes)
    return cipher.encrypt(text_bytes).decode()

def decrypt(encrypted_text : str, key : str):

    key_bytes = generate_key(key).encode()
    encrypted_text_bytes = encrypted_text.encode()

    cipher = Fernet(key_bytes)
    return cipher.decrypt(encrypted_text_bytes).decode()

def generate_key(rawkey : str):

    if len(rawkey) > 32:
        raise Exception("invalid key length, should less or equal 32")

    if len(rawkey) < 32:
        rawkey = rawkey.ljust(32, 'x')
        
    return base64.urlsafe_b64encode(rawkey.encode()).decode()

if __name__ == "__main__":

    import argparse

    parser = argparse.ArgumentParser("")

    parser.add_argument("-a", "--action", choices=["generate", "encrypt", "decrypt"], help="执行行为")
    parser.add_argument("-d", "--data", help="需要加解密数据")
    parser.add_argument("-k", "--key", help="密钥")

    parse = parser.parse_args()

    action = parse.action
    data = parse.data
    key = parse.key

    if action == "generate":
        g_key = generate_key(data)
        print(f"generate raw key: {data} -----> {g_key}")

    if action == "encrypt":
        encrypt_text = encrypt(data, key)
        print(f"encrypt of text:'{data}' by key:{key} -----> {encrypt_text}")

    if action == "decrypt":
        decrypt_text = decrypt(data, key)
        print(f"decrypt of text:'{data}' by key:{key} -----> {decrypt_text}")