from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from functools import wraps
from backend.db import SessionLocal, User, Route, Schedule, Reservation, Notice, Bono, UserBono

admin_bp = Blueprint("admin", __name__)

def current_user():
    uid = session.get("user_id")
    if not uid:
        return None
    db = SessionLocal()
    try:
        return db.query(User).get(uid)
    finally:
        db.close()

def admin_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        u = current_user()
        if not u or u.role != "admin":
            flash("Acceso restringido.", "error")
            return redirect(url_for("public.index"))
        return f(*args, **kwargs)
    return decorated

@admin_bp.route("/admin")
@admin_required
def admin():
    db = SessionLocal()
    try:
        stats = {
            "users":        db.query(User).count(),
            "routes":       db.query(Route).count(),
            "schedules":    db.query(Schedule).count(),
            "reservations": db.query(Reservation).count(),
        }
        reservations = db.query(Reservation).all()
        enriched = []
        for r in reservations:
            enriched.append({
                "id":               r.id,
                "locator":          r.locator,
                "seat":             r.seat,
                "price_paid":       r.price_paid,
                "discount_applied": r.discount_applied,
                "schedule": {
                    "date":      r.schedule.date,
                    "departure": r.schedule.departure,
                },
                "route": {
                    "origin":      r.schedule.route.origin,
                    "destination": r.schedule.route.destination,
                },
                "user": {
                    "name":  r.user.name,
                    "email": r.user.email,
                },
            })
        enriched.sort(key=lambda x: (x["schedule"]["date"], x["schedule"]["departure"]))
        notices = db.query(Notice).all()
        bonos   = db.query(Bono).all()
    finally:
        db.close()
    return render_template("admin.html", stats=stats, reservations=enriched,
                           notices=notices, bonos=bonos)

@admin_bp.route("/admin/reservation/<int:res_id>/delete", methods=["POST"])
@admin_required
def admin_delete_res(res_id):
    db = SessionLocal()
    try:
        r = db.query(Reservation).get(res_id)
        if r:
            db.delete(r)
            db.commit()
        flash("Reserva eliminada.", "success")
    finally:
        db.close()
    return redirect(url_for("admin.admin"))

@admin_bp.route("/admin/route/add", methods=["POST"])
@admin_required
def admin_add_route():
    orig  = request.form.get("origin", "").strip()
    dest  = request.form.get("destination", "").strip()
    dur   = request.form.get("duration", "").strip()
    price = float(request.form.get("price", 0))
    if orig and dest and dur and price > 0:
        db = SessionLocal()
        try:
            db.add(Route(origin=orig, destination=dest, duration=dur, price=price))
            db.commit()
            flash("Ruta añadida.", "success")
        finally:
            db.close()
    return redirect(url_for("admin.admin"))