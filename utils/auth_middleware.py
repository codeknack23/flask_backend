from flask import request, jsonify
from functools import wraps
import jwt
from config import Config

def auth_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.headers.get("Authorization")
        if not token:
            return jsonify({"error": "No token"}), 401
        try:
            token = token.split(" ")[1]
            decoded = jwt.decode(token, Config.SECRET_KEY, algorithms=["HS256"])
            request.user = decoded
        except Exception:
            return jsonify({"error": "Invalid token"}), 403
        return f(*args, **kwargs)
    return decorated
