"""
app.py — Servidor único de EuskoMove (puerto 3000)
Ejecutar desde la carpeta raíz del proyecto:
    python app.py
"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from flask import Flask, send_from_directory
from backend.routes.auth_routes    import auth_bp
from backend.routes.public_routes  import public_bp
from backend.routes.reservation_routes import res_bp
from backend.routes.notice_routes  import notice_bp
from backend.routes.admin_routes   import admin_bp
from backend.routes.bono_routes    import bono_bp

app = Flask(
    __name__,
    template_folder="frontend/templates",
    static_folder="frontend/static",
)
app.secret_key = "euskomove-secret-2025-eus"

app.register_blueprint(public_bp)
app.register_blueprint(auth_bp)
app.register_blueprint(res_bp)
app.register_blueprint(notice_bp)
app.register_blueprint(admin_bp)
app.register_blueprint(bono_bp)

if __name__ == "__main__":
    print("\n✅  EuskoMove en http://127.0.0.1:3000\n")
    app.run(debug=True, port=3000)
