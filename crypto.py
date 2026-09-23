import os
import base64
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.ciphers.aead import AESGCM


def generate_key(password, salt):
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,
        iterations=600000
    )

    return kdf.derive(password.encode())


def encrypt_text(text, password):
    salt = os.urandom(16)
    key = generate_key(password, salt)

    nonce = os.urandom(12)
    aes = AESGCM(key)

    encrypted = aes.encrypt(
        nonce,
        text.encode(),
        None
    )

    result = salt + nonce + encrypted

    return base64.b64encode(result).decode()


def decrypt_text(encrypted_text, password):
    try:
        data = base64.b64decode(encrypted_text)

        if len(data) < 29:
            raise ValueError("Invalid encrypted text.")

        salt = data[:16]
        nonce = data[16:28]
        encrypted = data[28:]

        key = generate_key(password, salt)

        aes = AESGCM(key)

        decrypted = aes.decrypt(
            nonce,
            encrypted,
            None
        )

        return decrypted.decode()

    except Exception:
        raise ValueError(
            "Wrong password or invalid encrypted text."
        )