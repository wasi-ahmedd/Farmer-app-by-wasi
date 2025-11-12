import time
import jwt
from functools import wraps
from flask import request, jsonify, current_app

def make_token(user_id, role):
    payload = {
        "sub": user_id,
        "role": role,
        "iat": int(time.time()),
        "exp": int(time.time()) + 60*60*24*7  # 7 days
    }
    return jwt.encode(payload, current_app.config["SECRET_KEY"], algorithm=current_app.config["JWT_ALGO"])

def decode_token(token):
    return jwt.decode(token, current_app.config["SECRET_KEY"], algorithms=[current_app.config["JWT_ALGO"]])

def auth_required(roles=None):
    def decorator(fn):
        @wraps(fn)
        def wrapper(*args, **kwargs):
            auth = request.headers.get("Authorization", "")
            if not auth.startswith("Bearer "):
                return jsonify({"error":"Missing/invalid Authorization header"}), 401
            token = auth.split(" ", 1)[1].strip()
            try:
                payload = decode_token(token)
            except Exception as e:
                return jsonify({"error": f"Invalid token: {e}"}), 401
            if roles and payload.get("role") not in roles:
                return jsonify({"error":"Insufficient role"}), 403
            request.user_id = payload.get("sub")
            request.user_role = payload.get("role")
            return fn(*args, **kwargs)
        return wrapper
    return decorator
