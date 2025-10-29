from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_wtf.csrf import CSRFProtect
from .config import Config

db = SQLAlchemy()
migrate = Migrate()
csrf = CSRFProtect()

def create_app(config_class: type[Config] = Config) -> Flask:
    app = Flask(__name__)
    app.config.from_object(config_class)

    db.init_app(app)
    migrate.init_app(app, db)
    csrf.init_app(app)

    from . import models  # noqa: F401 - ensure models are registered
    from .views import main_bp
    from .admin import admin_bp

    app.register_blueprint(main_bp)
    app.register_blueprint(admin_bp, url_prefix="/admin")

    @app.cli.command("create-defaults")
    def create_defaults() -> None:
        """Populate the database with starter content if it's empty."""
        from .seed import seed_defaults

        seed_defaults()
        print("Default content ensured.")

    return app
