from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from datetime import date
from backend.db import (SessionLocal, User, Route, Schedule, Reservation, Bono, UserBono,
                         get_booked_seats, available_seats, make_locator, use_bono_trip,
                         user_active_bono)

res_bp = Blueprint("res", __name__)

def current_user():
    uid = session.get("user_id")
    if not uid:
        return None
    db = SessionLocal()
    try:
        return db.query(User).get(uid)
    finally:
        db.close()

@res_bp.route("/book/<int:schedule_id>")
def book(schedule_id):
    user = current_user()
    if not user:
        return redirect(url_for("auth.login", next=request.url))
    db = SessionLocal()
    try:
        sch = db.query(Schedule).get(schedule_id)
        if not sch:
            flash("Servicio no encontrado.", "error")
            return redirect(url_for("public.search"))
        route    = db.query(Route).get(sch.route_id)
        booked   = get_booked_seats(schedule_id)
        passengers = int(request.args.get("passengers", 1))
        ub = user_active_bono(user.id)
        discount = 0.0
        if ub:
            bono = db.query(Bono).get(ub["bono_id"])
            discount = bono.discount if bono else 0.0
        return render_template("book.html",
            schedule={"id": sch.id, "date": sch.date,
                      "departure": sch.departure, "bus_code": sch.bus_code},
            route={"id": route.id, "origin": route.origin,
                   "destination": route.destination,
                   "duration": route.duration, "price": route.price},
            booked=booked, passengers=passengers, discount=discount)
    finally:
        db.close()

@res_bp.route("/book/<int:schedule_id>", methods=["POST"])
def do_book(schedule_id):
    user = current_user()
    if not user:
        return redirect(url_for("auth.login"))
    db = SessionLocal()
    try:
        sch = db.query(Schedule).get(schedule_id)
        if not sch:
            flash("Servicio no encontrado.", "error")
            return redirect(url_for("public.search"))
        route      = db.query(Route).get(sch.route_id)
        passengers = int(request.form.get("passengers", 1))
        seats      = request.form.getlist("seats")
        if len(seats) != passengers:
            flash(f"Debes seleccionar exactamente {passengers} asiento(s).", "error")
            return redirect(url_for("res.book", schedule_id=schedule_id, passengers=passengers))
        booked   = get_booked_seats(schedule_id)
        conflict = [s for s in seats if s in booked]
        if conflict:
            flash(f"Los asientos {', '.join(conflict)} ya están ocupados. Elige otros.", "error")
            return redirect(url_for("res.book", schedule_id=schedule_id, passengers=passengers))
        locs = []
        for seat in seats:
            disc       = use_bono_trip(user.id)
            price_paid = round(route.price * (1 - disc), 2)
            r = Reservation(
                user_id=user.id, schedule_id=schedule_id,
                seat=seat, locator=make_locator(),
                price_paid=price_paid, discount_applied=disc
            )
            db.add(r)
            db.flush()
            locs.append(r.locator)
        db.commit()
        flash(f"Reserva confirmada. Localizadores: {', '.join(locs)}", "success")
    finally:
        db.close()
    return redirect(url_for("res.my_trips"))

@res_bp.route("/my-trips")
def my_trips():
    user = current_user()
    if not user:
        return redirect(url_for("auth.login", next=url_for("res.my_trips")))
    db = SessionLocal()
    try:
        reservations = db.query(Reservation).filter_by(user_id=user.id).all()
        today = date.today().isoformat()
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
                    "bus_code":  r.schedule.bus_code,
                },
                "route": {
                    "origin":      r.schedule.route.origin,
                    "destination": r.schedule.route.destination,
                    "duration":    r.schedule.route.duration,
                    "price":       r.schedule.route.price,
                },
            })
        enriched.sort(key=lambda x: (x["schedule"]["date"], x["schedule"]["departure"]))
    finally:
        db.close()
    return render_template("my_trips.html", reservations=enriched, today=today)

@res_bp.route("/cancel/<int:res_id>", methods=["POST"])
def cancel(res_id):
    user = current_user()
    db = SessionLocal()
    try:
        r = db.query(Reservation).get(res_id)
        if not r or (r.user_id != user.id and user.role != "admin"):
            flash("No autorizado.", "error")
        else:
            db.delete(r)
            db.commit()
            flash("Reserva cancelada.", "success")
    finally:
        db.close()
    return redirect(url_for("res.my_trips"))