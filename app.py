"""
app.py — Servidor único de EuskoMove (puerto 3000)
Ejecutar desde la carpeta raíz del proyecto:
    python app.py
"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from flask import Flask, send_from_directory
from flask_talisman import Talisman

from backend.routes.auth_routes import auth_bp
from backend.routes.public_routes import public_bp
from backend.routes.reservation_routes import res_bp
from backend.routes.notice_routes import notice_bp
from backend.routes.admin_routes import admin_bp
from backend.routes.bono_routes import bono_bp
from backend.db import init_db

app = Flask(
    __name__,
    template_folder="frontend/templates",
    static_folder="frontend/static",
)

# ─── CONFIGURACIÓN DE SEGURIDAD CON FLASK-TALISMAN ───────────────────────────
# Forzar HTTPS solo en producción (en local con debug=True nos dejará usar http://)
is_production = os.environ.get("FLASK_ENV") == "production"

Talisman(
    app,
    force_https=is_production,  # Fuerza HTTPS solo cuando la app corre en Azure
    content_security_policy=None # Ponemos None inicialmente para evitar que bloquee scripts locales en tu frontend académico
)
# ─────────────────────────────────────────────────────────────────────────────

app.secret_key = os.environ.get("FLASK_SECRET_KEY", "euskomove-secret-2025-eus")

with app.app_context():
    init_db()

@app.context_processor
def inject_current_user():
    def current_user():
        return None
    return dict(current_user=current_user)


app.register_blueprint(public_bp)
app.register_blueprint(auth_bp)
app.register_blueprint(res_bp)
app.register_blueprint(notice_bp)
app.register_blueprint(admin_bp)
app.register_blueprint(bono_bp)


if __name__ == "__main__":
    print("\n   EuskoMove en http://127.0.0.1:3000\n")
    app.run(debug=True, port=3000)