import os
from flask import Flask
from config import config_by_name, Config
from app.utils.extensions import db, migrate

def create_app(config_name=None):
    if config_name is None:
        config_name = os.environ.get("FLASK_ENV", "development")

    flask_app = Flask(__name__)
    if isinstance(config_name, str):
        config_obj = config_by_name.get(config_name, Config)
    else:
        config_obj = config_name or Config
    flask_app.config.from_object(config_obj)

    # Initialize extensions
    db.init_app(flask_app)
    migrate.init_app(flask_app, db)

    # Register blueprints
    from app.routes.main import main_bp
    from app.routes.api import api_bp

    flask_app.register_blueprint(main_bp)
    flask_app.register_blueprint(api_bp)

    with flask_app.app_context():
        from app.models import Ticket, AnalysisLog  # noqa: F401
        db.create_all()

    return flask_app
