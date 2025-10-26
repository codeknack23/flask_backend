from flask import request, jsonify
from functools import wraps
import jwt
from config import Config

def auth_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.headers.get("Authorization")
        if not token:
            # ✅ Return JSON 401, no redirect
            return jsonify({"error": "No token provided"}), 401

        try:
            # Split "Bearer <token>"
            token = token.split(" ")[1]
            decoded = jwt.decode(token, Config.SECRET_KEY, algorithms=["HS256"])
            request.user = decoded
        except jwt.ExpiredSignatureError:
            return jsonify({"error": "Token expired"}), 401
        except jwt.InvalidTokenError:
            return jsonify({"error": "Invalid token"}), 401
        except Exception as e:
            return jsonify({"error": str(e)}), 401

        return f(*args, **kwargs)
    return decorated
