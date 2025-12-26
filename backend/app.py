from flask import Flask
from flask_cors import CORS
from backend.config import Config
from backend.db import db
from backend.routes.users import bp_users, bcrypt
from backend.routes.crops import bp_crops
from backend.routes.market import bp_market
from backend.routes.admin import admin_bp


def create_app():
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_object(Config)

    # ✅ FIXED CORS (Netlify + Local + Auth safe)
    CORS(
        app,
        resources={r"/api/*": {"origins": [
            "https://farmerappbywasi.netlify.app",
            "http://localhost:5500",
            "http://127.0.0.1:5500"
        ]}},
        supports_credentials=True
    )

    # Initialize DB and bcrypt
    db.init_app(app)
    bcrypt.init_app(app)
    with app.app_context():
        db.create_all()
    #Health check
    @app.route("/")
    def home():
        return {
            "status": "ok",
            "message": "Farmer App backend is running"
        }

    # Register blueprints
    app.register_blueprint(bp_users)
    app.register_blueprint(bp_crops)
    app.register_blueprint(bp_market)
    app.register_blueprint(admin_bp)

    return app


# Expose app for Gunicorn
app = create_app()
