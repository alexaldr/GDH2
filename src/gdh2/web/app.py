from __future__ import annotations

from flask import Flask

from gdh2.settings import settings
from gdh2.web.routes.health import bp as health_bp


def create_app() -> Flask:
    app = Flask(__name__)
    app.config["SECRET_KEY"] = settings.SECRET_KEY

    app.register_blueprint(health_bp)

    return app


# Flask CLI entrypoint
app = create_app()
