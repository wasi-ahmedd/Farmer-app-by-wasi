from flask import Flask
from flask_cors import CORS
from backend.config import Config
from backend.db import db
from backend.routes.users import bp_users, bcrypt
from backend.routes.crops import bp_crops
from backend.routes.market import bp_market
from backend.models import User, CropPlan
from backend.routes.admin import admin_bp  # ✅ Import admin blueprint

@app.route("/")
def home():
    return {
        "status": "ok",
        "message": "Farmer App backend is running"
    }

def create_app():
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_object(Config)

    # Enable CORS
    CORS(app, resources={r"/api/*": {"origins": app.config["CORS_ORIGINS"]}})

    # Initialize DB and bcrypt
    db.init_app(app)
    bcrypt.init_app(app)

    with app.app_context():
        db.create_all()

    # ✅ Register all blueprints here (AFTER app is defined)
    app.register_blueprint(bp_users)
    app.register_blueprint(bp_crops)
    app.register_blueprint(bp_market)
    app.register_blueprint(admin_bp)

    return app


# ✅ Define app instance
app = create_app()

# if __name__ == "__main__":
#     from backend.app import app
#     app.run(host="0.0.0.0", port=5000)



