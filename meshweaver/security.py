import hashlib
import hmac
import json
import os


SECRET_KEY = os.getenv(
    "MESHWEAVER_SECRET_KEY",
    "meshweaver-secret-key"
).encode("utf-8")


def sign_message(message):
    data = json.dumps(message, sort_keys=True).encode("utf-8")

    signature = hmac.new(
        SECRET_KEY,
        data,
        hashlib.sha256
    ).hexdigest()

    return signature


def verify_message(message, signature):
    expected_signature = sign_message(message)

    return hmac.compare_digest(
        expected_signature,
        signature
    )