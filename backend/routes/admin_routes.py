from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from backend.db import USERS, ROUTES, SCHEDULES, RESERVATIONS, NOTICES, BONOS, USER_BONOS, next_rid

admin_bp = Blueprint("admin", __name__)

def current_user():
    uid = session.get("user_id")
    return USERS.get(uid)

def admin_required(f):
    from functools import wraps
    @wraps(f)
    def decorated(*args, **kwargs):
        u = current_user()
        if not u or u.get("role") != "admin":
            flash("Acceso restringido.", "error")
            return redirect(url_for("public.index"))
        return f(*args, **kwargs)
    return decorated

@admin_bp.route("/admin")
@admin_required
def admin():
    stats = {"users":len(USERS),"routes":len(ROUTES),
             "schedules":len(SCHEDULES),"reservations":len(RESERVATIONS)}
    enriched = []
    for r in RESERVATIONS.values():
        sch   = SCHEDULES[r["schedule_id"]]
        route = ROUTES[sch["route_id"]]
        user  = USERS.get(r["user_id"],{})
        enriched.append({**r,"schedule":sch,"route":route,"user":user})
    enriched.sort(key=lambda x:(x["schedule"]["date"],x["schedule"]["departure"]))
    return render_template("admin.html", stats=stats, reservations=enriched,
                           notices=list(NOTICES.values()), bonos=list(BONOS.values()))

@admin_bp.route("/admin/reservation/<int:res_id>/delete", methods=["POST"])
@admin_required
def admin_delete_res(res_id):
    RESERVATIONS.pop(res_id, None)
    flash("Reserva eliminada.", "success")
    return redirect(url_for("admin.admin"))

@admin_bp.route("/admin/route/add", methods=["POST"])
@admin_required
def admin_add_route():
    rid   = next_rid()
    orig  = request.form.get("origin","").strip()
    dest  = request.form.get("destination","").strip()
    dur   = request.form.get("duration","").strip()
    price = float(request.form.get("price",0))
    if orig and dest and dur and price>0:
        ROUTES[rid] = {"id":rid,"origin":orig,"destination":dest,"duration":dur,"price":price}
        flash("Ruta añadida.", "success")
    return redirect(url_for("admin.admin"))
