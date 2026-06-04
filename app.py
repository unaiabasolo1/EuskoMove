"""
app.py — Servidor único de EuskoMove (puerto 3000)
Ejecutar desde la carpeta raíz del proyecto:
    python app.py
"""
import sys
import os
import logging

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from flask import Flask
from flask_talisman import Talisman

from backend.routes.auth_routes import auth_bp, current_user
from backend.routes.public_routes import public_bp
from backend.routes.reservation_routes import res_bp
from backend.routes.notice_routes import notice_bp
from backend.routes.admin_routes import admin_bp
from backend.routes.bono_routes import bono_bp
from backend.db import init_db

# ─── CONFIGURACIÓN DE LOGGING ────────────────────────────────────────────────
_nivel = os.environ.get("LOG_LEVEL", "INFO").upper()
logging.basicConfig(
    level=getattr(logging, _nivel, logging.INFO),
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    handlers=[logging.StreamHandler(sys.stdout)],
)
logger = logging.getLogger("euskomove")
logger.info("Inicializando aplicación EuskoMove (nivel de log: %s)", _nivel)

app = Flask(
    __name__,
    template_folder="frontend/templates",
    static_folder="frontend/static",
)

# ─── CONFIGURACIÓN DE SEGURIDAD CON FLASK-TALISMAN ───────────────────────────
is_production = os.environ.get("FLASK_ENV") == "production"

Talisman(
    app,
    force_https=is_production,
    content_security_policy=None,
)

# ─── SECRET KEY DESDE VARIABLES DE ENTORNO ───────────────────────────────────
app.secret_key = os.environ.get("FLASK_SECRET_KEY")
if not app.secret_key:
    logger.error("FLASK_SECRET_KEY no está configurado: la app no puede arrancar")
    raise RuntimeError("FLASK_SECRET_KEY no está configurado")

with app.app_context():
    try:
        init_db()
        logger.info("Base de datos inicializada correctamente")
    except Exception as e:
        logger.error("Error inicializando la base de datos: %s", e)
        raise

@app.context_processor
def inject_current_user():
    return dict(current_user=current_user)

app.register_blueprint(public_bp)
app.register_blueprint(auth_bp)
app.register_blueprint(res_bp)
app.register_blueprint(notice_bp)
app.register_blueprint(admin_bp)
app.register_blueprint(bono_bp)

if __name__ == "__main__":
    logger.debug("Arrancando servidor de desarrollo en el puerto 3000")
    print("\n   EuskoMove en http://127.0.0.1:3000\n")
    app.run(debug=True, port=3000)