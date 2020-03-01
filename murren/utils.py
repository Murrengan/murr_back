import hashlib
import hmac
from uuid import uuid4
import crypt


def create_token_reset_password():
    key = str(uuid4())
    hashed = crypt.mksalt(crypt.METHOD_SHA512)
    token = hmac.new(key.encode(), hashed.encode(), hashlib.sha256).hexdigest()

    return token
