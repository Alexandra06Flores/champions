import os
from flask import Flask
from app.data.db import init_db
from app.presentation.routes import bp
from app.business import services


def create_app():
    app = Flask(__name__)
    app.secret_key = os.getenv("SECRET_KEY", "dev-secret")
    app.register_blueprint(bp)

    # Al iniciar: crear tablas y guardar los partidos recuperados de la API
    init_db()
    services.sync_matches()
    return app
