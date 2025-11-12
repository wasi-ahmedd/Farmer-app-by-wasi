from flask import Blueprint, jsonify, request
from backend.db import db
from backend.models import User, CropPlan

admin_bp = Blueprint("admin", __name__, url_prefix="/api/admin")

# ✅ Main stats route with filters
@admin_bp.route("/stats")
def stats():
    crop_filter = request.args.get("crop")
    state_filter = request.args.get("state")
    district_filter = request.args.get("district")

    # Base queries
    farmer_query = User.query.filter_by(role="farmer")
    customer_query = User.query.filter_by(role="customer")
    crop_query = CropPlan.query

    # Apply filters (region-wise)
    if state_filter:
        farmer_query = farmer_query.filter(User.state == state_filter)
        crop_query = crop_query.filter(CropPlan.state == state_filter)
    if district_filter:
        farmer_query = farmer_query.filter(User.district == district_filter)
        crop_query = crop_query.filter(CropPlan.district == district_filter)
    if crop_filter:
        crop_query = crop_query.filter(CropPlan.crop.ilike(f"%{crop_filter}%"))

    farmers = farmer_query.count()
    customers = customer_query.count()
    crops = crop_query.count()

    # Demand stats per crop (with filters)
    results = (
        crop_query.with_entities(
            CropPlan.crop,
            db.func.count(CropPlan.id).label("farmers"),
            db.func.sum(CropPlan.quantity).label("quantity")
        )
        .group_by(CropPlan.crop)
        .all()
    )

    demand = []
    for row in results:
        q = row.quantity or 0
        demand_level = "High" if q < 500 else "Medium" if q < 2000 else "Low"
        demand.append({
            "crop": row.crop,
            "farmers": row.farmers,
            "quantity": q,
            "demand_level": demand_level
        })

    return jsonify({
        "farmers": farmers,
        "customers": customers,
        "crops": crops,
        "demand": demand
    })


# ✅ Get users by role (farmer / customer)
@admin_bp.route("/users/<role>")
def get_users(role):
    users = User.query.filter_by(role=role).all()
    return jsonify([
        {
            "id": u.id,
            "username": u.username,
            "state": u.state,
            "district": u.district,
            "village": u.village,
            "contact": getattr(u, "contact", "")
        }
        for u in users
    ])


# ✅ Get crops (with farmer names + optional filters)
@admin_bp.route("/crops")
def get_crops():
    crop_filter = request.args.get("crop")
    state_filter = request.args.get("state")
    district_filter = request.args.get("district")

    query = db.session.query(CropPlan, User.username).join(User, CropPlan.farmer_id == User.id)

    if crop_filter:
        query = query.filter(CropPlan.crop.ilike(f"%{crop_filter}%"))
    if state_filter:
        query = query.filter(CropPlan.state == state_filter)
    if district_filter:
        query = query.filter(CropPlan.district == district_filter)

    crops = query.all()
    return jsonify([
        {
            "id": c.CropPlan.id,
            "farmer_name": c.username,
            "crop": c.CropPlan.crop,
            "quantity": c.CropPlan.quantity,
            "harvest_date": c.CropPlan.harvest_date,
            "state": c.CropPlan.state,
            "district": c.CropPlan.district,
            "village": c.CropPlan.village,
        }
        for c in crops
    ])
