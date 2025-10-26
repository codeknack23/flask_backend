from functools import wraps
from flask import request, jsonify
import jwt
from config import Config

def auth_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        # ✅ Allow preflight OPTIONS requests to pass without auth
        if request.method == "OPTIONS":
            return '', 200

        auth_header = request.headers.get("Authorization")
        if not auth_header:
            return jsonify({"error": "No token"}), 401

        try:
            token = auth_header.split(" ")[1]  # Expect 'Bearer <token>'
            decoded = jwt.decode(token, Config.SECRET_KEY, algorithms=["HS256"])
            request.user = decoded
        except Exception:
            return jsonify({"error": "Invalid token"}), 403

        return f(*args, **kwargs)
    return decorated
