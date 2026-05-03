from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from datetime import date
from backend.db import (ROUTES, SCHEDULES, RESERVATIONS, BONOS, USER_BONOS,
                         get_booked_seats, available_seats, make_locator,
                         use_bono_trip, user_active_bono)

res_bp = Blueprint("res", __name__)

def current_user():
    from backend.db import USERS
    uid = session.get("user_id")
    return USERS.get(uid)

_res_counter = {"v": 1}
def next_res_id():
    v = _res_counter["v"]; _res_counter["v"] += 1; return v

@res_bp.route("/book/<int:schedule_id>")
def book(schedule_id):
    user = current_user()
    if not user:
        return redirect(url_for("auth.login", next=request.url))
    sch   = SCHEDULES.get(schedule_id)
    if not sch:
        flash("Servicio no encontrado.", "error")
        return redirect(url_for("public.search"))
    route    = ROUTES[sch["route_id"]]
    booked   = get_booked_seats(schedule_id)
    passengers = int(request.args.get("passengers", 1))
    ub = user_active_bono(user["id"])
    discount = BONOS[ub["bono_id"]]["discount"] if ub else 0.0
    return render_template("book.html", schedule=sch, route=route,
                           booked=booked, passengers=passengers, discount=discount)

@res_bp.route("/book/<int:schedule_id>", methods=["POST"])
def do_book(schedule_id):
    user = current_user()
    if not user:
        return redirect(url_for("auth.login"))
    sch   = SCHEDULES.get(schedule_id)
    if not sch:
        flash("Servicio no encontrado.", "error")
        return redirect(url_for("public.search"))
    route      = ROUTES[sch["route_id"]]
    passengers = int(request.form.get("passengers", 1))
    seats      = request.form.getlist("seats")
    if len(seats) != passengers:
        flash(f"Debes seleccionar exactamente {passengers} asiento(s).", "error")
        return redirect(url_for("res.book", schedule_id=schedule_id, passengers=passengers))
    booked = get_booked_seats(schedule_id)
    conflict = [s for s in seats if s in booked]
    if conflict:
        flash(f"Los asientos {', '.join(conflict)} ya están ocupados. Elige otros.", "error")
        return redirect(url_for("res.book", schedule_id=schedule_id, passengers=passengers))
    # Crear una reserva por asiento
    locs = []
    for seat in seats:
        disc = use_bono_trip(user["id"])
        price_paid = round(route["price"] * (1 - disc), 2)
        rid = next_res_id()
        RESERVATIONS[rid] = {
            "id": rid, "user_id": user["id"], "schedule_id": schedule_id,
            "seat": seat, "locator": make_locator(),
            "price_paid": price_paid, "discount_applied": disc,
        }
        locs.append(RESERVATIONS[rid]["locator"])
    flash(f"✅ Reserva confirmada. Localizadores: {', '.join(locs)}", "success")
    return redirect(url_for("res.my_trips"))

@res_bp.route("/my-trips")
def my_trips():
    user = current_user()
    if not user:
        return redirect(url_for("auth.login", next=url_for("res.my_trips")))
    today = date.today().isoformat()
    mine  = [r for r in RESERVATIONS.values() if r["user_id"] == user["id"]]
    enriched = []
    for r in mine:
        sch   = SCHEDULES[r["schedule_id"]]
        route = ROUTES[sch["route_id"]]
        enriched.append({**r, "schedule": sch, "route": route})
    enriched.sort(key=lambda x: (x["schedule"]["date"], x["schedule"]["departure"]))
    return render_template("my_trips.html", reservations=enriched, today=today)

@res_bp.route("/cancel/<int:res_id>", methods=["POST"])
def cancel(res_id):
    user = current_user()
    res  = RESERVATIONS.get(res_id)
    if not res or (res["user_id"] != user["id"] and user.get("role") != "admin"):
        flash("No autorizado.", "error")
    else:
        RESERVATIONS.pop(res_id)
        flash("Reserva cancelada.", "success")
    return redirect(url_for("res.my_trips"))
