from datetime import datetime
from backend.db import db

# Users: farmer or customer
class User(db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, index=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)
    role = db.Column(db.String(16), nullable=False)  # "farmer" or "customer"
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # optional contact/location fields (handy for buyers to see)
    state = db.Column(db.String(64))
    district = db.Column(db.String(64))
    taluk = db.Column(db.String(64))
    village = db.Column(db.String(64))
    contact = db.Column(db.String(32))

# Crop plans made by farmers
class CropPlan(db.Model):
    __tablename__ = "crop_plans"
    id = db.Column(db.Integer, primary_key=True)
    farmer_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    crop = db.Column(db.String(64), nullable=False)
    quantity = db.Column(db.Float, nullable=False)
    sow_date = db.Column(db.String(32), nullable=False)
    harvest_date = db.Column(db.String(32), nullable=False)
    state = db.Column(db.String(64), nullable=False)
    district = db.Column(db.String(64), nullable=False)
    taluk = db.Column(db.String(64), nullable=False)
    village = db.Column(db.String(64), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    farmer = db.relationship("User", backref=db.backref("plans", lazy=True))
