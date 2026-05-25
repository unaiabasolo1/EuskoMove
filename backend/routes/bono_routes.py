from flask import Blueprint, redirect, url_for, flash, session, request
from datetime import date
from backend.db import SessionLocal, Bono, UserBono

bono_bp = Blueprint("bono", __name__)

def current_user():
    from backend.db import User
    uid = session.get("user_id")
    if not uid:
        return None
    db = SessionLocal()
    try:
        return db.query(User).get(uid)
    finally:
        db.close()

@bono_bp.route("/bonos/buy/<int:bono_id>", methods=["POST"])
def buy_bono(bono_id):
    user = current_user()
    if not user:
        return redirect(url_for("auth.login", next=url_for("public.bonos")))
    db = SessionLocal()
    try:
        bono = db.query(Bono).get(bono_id)
        if not bono:
            flash("Bono no encontrado.", "error")
            return redirect(url_for("public.bonos"))
        db.add(UserBono(
            user_id=user.id,
            bono_id=bono_id,
            trips_left=bono.trips,
            purchased_at=date.today().isoformat()
        ))
        db.commit()
        flash(f"✅ {bono.name} activado. Tienes {bono.trips} viajes disponibles.", "success")
    finally:
        db.close()
    return redirect(url_for("public.bonos"))