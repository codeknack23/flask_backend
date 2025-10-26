from flask import request, jsonify
from functools import wraps
import jwt
from config import Config

def auth_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        # Allow preflight requests to pass through
        if request.method == "OPTIONS":
            return jsonify({}), 200

        token = request.headers.get("Authorization")
        if not token:
            return jsonify({"error": "No token provided"}), 401
        try:
            # Bearer token expected
            token = token.split(" ")[1]
            decoded = jwt.decode(token, Config.SECRET_KEY, algorithms=["HS256"])
            request.user = decoded
        except Exception as e:
            print("JWT decode error:", e)
            return jsonify({"error": "Invalid or expired token"}), 403
        return f(*args, **kwargs)
    return decorated
