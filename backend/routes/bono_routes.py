from flask import Blueprint, redirect, url_for, flash, session, request
from backend.db import BONOS, USER_BONOS

bono_bp = Blueprint("bono", __name__)

def current_user():
    from backend.db import USERS
    uid = session.get("user_id")
    return USERS.get(uid)

@bono_bp.route("/bonos/buy/<int:bono_id>", methods=["POST"])
def buy_bono(bono_id):
    user = current_user()
    if not user:
        return redirect(url_for("auth.login", next=url_for("public.bonos")))
    bono = BONOS.get(bono_id)
    if not bono:
        flash("Bono no encontrado.", "error")
        return redirect(url_for("public.bonos"))
    from datetime import date
    USER_BONOS.setdefault(user["id"], []).append({
        "bono_id": bono_id, "trips_left": bono["trips"],
        "purchased_at": date.today().isoformat(),
    })
    flash(f"✅ {bono['name']} activado. Tienes {bono['trips']} viajes disponibles.", "success")
    return redirect(url_for("public.bonos"))
