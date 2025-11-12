from flask import Blueprint, request, jsonify
from datetime import datetime
from backend.db import db
from backend.models import CropPlan, User

bp_market = Blueprint("market", __name__, url_prefix="/api/market")

@bp_market.route("/search", methods=["GET"])
def search_crops():
    crop = request.args.get("crop", "").lower()
    state = request.args.get("state", "").lower()
    district = request.args.get("district", "").lower()
    date_str = request.args.get("date", "")

    # Date filter (±7 days)
    date_filter = None
    if date_str:
        try:
            date_filter = datetime.strptime(date_str, "%Y-%m-%d")
        except ValueError:
            date_filter = None

    query = db.session.query(CropPlan, User).join(User, CropPlan.farmer_id == User.id)
    results = []

    for c, u in query.all():
        harvest = None
        try:
            harvest = datetime.strptime(c.harvest_date, "%Y-%m-%d")
        except:
            pass

        if (
            (not crop or crop == c.crop.lower()) and
            (not state or state == c.state.lower()) and
            (not district or district == c.district.lower()) and
            (not date_filter or (harvest and abs((harvest - date_filter).days) <= 7))
        ):
            results.append({
                "id": c.id,
                "crop": c.crop,
                "quantity": c.quantity,
                "harvest_date": c.harvest_date,
                "village": c.village,
                "district": c.district,
                "state": c.state,
                "farmer": {
                    "username": u.username,
                    "contact": getattr(u, "contact", "N/A")
                }
            })

    return jsonify(results)
