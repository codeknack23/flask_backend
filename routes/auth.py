from flask import Blueprint, request, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
from models import db, User
import jwt, datetime
from config import Config

auth_bp = Blueprint("auth_bp", __name__)

@auth_bp.route("/register", methods=["POST"])
def register():
    data = request.get_json()
    email = data.get("email")
    password = data.get("password")

    if User.query.filter_by(email=email).first():
        return jsonify({"error": "User exists"}), 400

    hashed = generate_password_hash(password)
    user = User(email=email, password=hashed)
    db.session.add(user)
    db.session.commit()
    return jsonify({"message": "User registered successfully"})


@auth_bp.route("/login", methods=["POST"])
def login():
    data = request.get_json()
    email = data.get("email")
    password = data.get("password")

    user = User.query.filter_by(email=email).first()
    if not user or not check_password_hash(user.password, password):
        return jsonify({"error": "Invalid credentials"}), 400

    token = jwt.encode(
        {"id": user.id, "email": user.email, "exp": datetime.datetime.utcnow() + datetime.timedelta(hours=1)},
        Config.SECRET_KEY,
        algorithm="HS256",
    )
    return jsonify({"token": token})
