from flask import Blueprint, request, jsonify
from backend.db import db
from backend.models import CropPlan, User
from backend.schemas import require_fields
from backend.auth import auth_required

bp_crops = Blueprint("crops", __name__, url_prefix="/api/crops")

# 🌾 Farmer creates a crop plan
@bp_crops.post("")
@auth_required(roles=["farmer"])
def create_plan():
    data = request.get_json(force=True, silent=True) or {}
    required = ["crop", "quantity", "sow_date", "harvest_date", "state", "district", "taluk", "village"]
    miss = require_fields(data, required)
    if miss:
        return jsonify({"error": f"Missing: {', '.join(miss)}"}), 400

    try:
        qty = float(data["quantity"])
    except:
        return jsonify({"error": "quantity must be a number"}), 400

    plan = CropPlan(
        farmer_id=request.user_id,
        crop=data["crop"].strip(),
        quantity=qty,
        sow_date=data["sow_date"].strip(),
        harvest_date=data["harvest_date"].strip(),
        state=data["state"].strip(),
        district=data["district"].strip(),
        taluk=data["taluk"].strip(),
        village=data["village"].strip(),
    )
    db.session.add(plan)
    db.session.commit()
    return jsonify({"message": "plan created", "id": plan.id}), 201


# 👨‍🌾 Farmer's own crop plans
@bp_crops.get("/mine")
@auth_required(roles=["farmer"])
def my_plans():
    plans = CropPlan.query.filter_by(farmer_id=request.user_id).order_by(CropPlan.id.desc()).all()
    return jsonify([_serialize_plan(p) for p in plans]), 200


# 🧑‍🤝‍🧑 Public crop search for customers (with filters)
@bp_crops.get("")
def search_plans():
    crop_name = (request.args.get("crop") or "").strip().lower()
    state = (request.args.get("state") or "").strip()
    district = (request.args.get("district") or "").strip()

    query = CropPlan.query.join(User)

    # Apply filters dynamically
    if crop_name:
        like = f"%{crop_name}%"
        query = query.filter(CropPlan.crop.ilike(like))
    if state:
        query = query.filter(CropPlan.state == state)
    if district:
        query = query.filter(CropPlan.district == district)

    query = query.order_by(CropPlan.harvest_date.asc())
    plans = query.limit(200).all()

    results = []
    for p in plans:
        results.append({
            "id": p.id,
            "crop": p.crop,
            "quantity": p.quantity,
            "sow_date": p.sow_date,
            "harvest_date": p.harvest_date,
            "state": p.state,
            "district": p.district,
            "taluk": p.taluk,
            "village": p.village,
            "farmer": {
                "username": p.farmer.username,
                "contact": p.farmer.contact
            } if p.farmer else None
        })

    return jsonify(results), 200

@bp_crops.route("/api/crops", methods=["GET"])
def get_crops():
    crop_name = request.args.get("crop")
    state = request.args.get("state")
    district = request.args.get("district")

    query = CropPlan.query
    if crop_name:
        query = query.filter(CropPlan.crop.ilike(f"%{crop_name}%"))
    if state:
        query = query.filter(CropPlan.state == state)
    if district:
        query = query.filter(CropPlan.district == district)

    crops = query.all()
    return jsonify([crop.to_dict() for crop in crops])

# 🧩 Helper function
def _serialize_plan(p: CropPlan):
    return {
        "id": p.id,
        "crop": p.crop,
        "quantity": p.quantity,
        "sow_date": p.sow_date,
        "harvest_date": p.harvest_date,
        "state": p.state,
        "district": p.district,
        "taluk": p.taluk,
        "village": p.village,
        "farmer_id": p.farmer_id,
    }
