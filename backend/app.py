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

    # Enable CORS
    CORS(app, resources={r"/api/*": {"origins": app.config.get("CORS_ORIGINS", "*")}})

    # Initialize DB and bcrypt
    db.init_app(app)
    bcrypt.init_app(app)

    # ❌ DO NOT create tables on startup in production
    # with app.app_context():
    #     db.create_all()

    # Health / root route (Railway needs fast response)
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
