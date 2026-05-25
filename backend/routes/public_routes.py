from flask import Blueprint, render_template, request, session
from datetime import date
from backend.db import SessionLocal, Route, Schedule, Notice, Bono, UserBono, available_seats, user_active_bono

public_bp = Blueprint("public", __name__)

CITIES = ["Vitoria-Gasteiz", "Bilbao", "Donostia-S.S."]

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

@public_bp.context_processor
def inject_globals():
    db = SessionLocal()
    try:
        active_notices = db.query(Notice).filter_by(active=True).all()
    finally:
        db.close()
    return dict(current_user=current_user, CITIES=CITIES,
                today=date.today().isoformat(), active_notices=active_notices)

@public_bp.route("/")
def index():
    return render_template("index.html")

@public_bp.route("/search")
def search():
    origin      = request.args.get("origin", "").strip()
    destination = request.args.get("destination", "").strip()
    travel_date = request.args.get("date", date.today().isoformat())
    passengers  = int(request.args.get("passengers", 1))
    today       = date.today().isoformat()
    max_date    = date.today().replace(year=date.today().year + 1).isoformat()
    results = []

    if origin and destination and origin != destination:
        db = SessionLocal()
        try:
            route = db.query(Route).filter_by(origin=origin, destination=destination).first()
            if route:
                schedules = db.query(Schedule).filter_by(
                    route_id=route.id, date=travel_date
                ).all()
                user = current_user()
                for sch in schedules:
                    avail = available_seats(sch.id)
                    if avail >= passengers:
                        discount = 0.0
                        if user:
                            ub = user_active_bono(user.id)
                            if ub:
                                bono_db = SessionLocal()
                                try:
                                    from backend.db import Bono
                                    b = bono_db.query(Bono).get(ub["bono_id"])
                                    discount = b.discount if b else 0.0
                                finally:
                                    bono_db.close()
                        total = round(route.price * passengers * (1 - discount), 2)
                        results.append({
                            "schedule": {"id": sch.id, "date": sch.date,
                                         "departure": sch.departure, "bus_code": sch.bus_code},
                            "route":    {"id": route.id, "origin": route.origin,
                                         "destination": route.destination,
                                         "duration": route.duration, "price": route.price},
                            "available":    avail,
                            "total_price":  total,
                            "discount":     discount,
                        })
            results.sort(key=lambda x: x["schedule"]["departure"])
        finally:
            db.close()

    return render_template("search.html",
        origin=origin, destination=destination, travel_date=travel_date,
        passengers=passengers, results=results,
        min_date=today, max_date=max_date)

@public_bp.route("/avisos")
def avisos():
    db = SessionLocal()
    try:
        notices = db.query(Notice).all()
    finally:
        db.close()
    return render_template("avisos.html", notices=notices)

@public_bp.route("/bonos")
def bonos():
    user = current_user()
    db = SessionLocal()
    try:
        all_bonos = db.query(Bono).all()
        my_bonos = []
        if user:
            my_bonos = db.query(UserBono).filter_by(user_id=user.id).all()
    finally:
        db.close()
    return render_template("bonos.html", bonos=all_bonos, my_bonos=my_bonos)