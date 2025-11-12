from flask import Blueprint, request, jsonify
from flask_bcrypt import Bcrypt
from backend.db import db
from backend.models import User
from backend.schemas import require_fields
from backend.auth import make_token

bp_users = Blueprint("users", __name__, url_prefix="/api/auth")
bcrypt = Bcrypt()

@bp_users.post("/signup")
def signup():
    data = request.get_json(force=True, silent=True) or {}
    required = ["username", "password", "role"]
    miss = require_fields(data, required)
    if miss: return jsonify({"error": f"Missing: {', '.join(miss)}"}), 400
    if data["role"] not in ("farmer","customer"):
        return jsonify({"error":"role must be 'farmer' or 'customer'"}), 400

    if User.query.filter_by(username=data["username"]).first():
        return jsonify({"error":"username already exists"}), 409

    pw_hash = bcrypt.generate_password_hash(data["password"]).decode("utf-8")
    user = User(
        username=data["username"],
        password_hash=pw_hash,
        role=data["role"],
        state=data.get("state"),
        district=data.get("district"),
        taluk=data.get("taluk"),
        village=data.get("village"),
        contact=data.get("contact"),
    )
    db.session.add(user)
    db.session.commit()
    token = make_token(user.id, user.role)
    return jsonify({"token": token, "user":{"id":user.id,"username":user.username,"role":user.role}}), 201

@bp_users.post("/login")
def login():
    data = request.get_json(force=True, silent=True) or {}
    miss = require_fields(data, ["username","password"])
    if miss: return jsonify({"error": f"Missing: {', '.join(miss)}"}), 400
    user = User.query.filter_by(username=data["username"]).first()
    if not user: return jsonify({"error":"invalid credentials"}), 401

    bcrypt_inst = Bcrypt()
    if not bcrypt_inst.check_password_hash(user.password_hash, data["password"]):
        return jsonify({"error":"invalid credentials"}), 401

    token = make_token(user.id, user.role)
    return jsonify({"token": token, "user":{"id":user.id,"username":user.username,"role":user.role}}), 200
