from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from datetime import date
from backend.db import (CITIES, ROUTES, SCHEDULES, RESERVATIONS, BONOS, NOTICES,
                         USER_BONOS, available_seats, user_active_bono)

public_bp = Blueprint("public", __name__)

def current_user():
    from backend.db import USERS
    uid = session.get("user_id")
    return USERS.get(uid)

@public_bp.context_processor
def inject_globals():
    today = date.today().isoformat()
    active_notices = [n for n in NOTICES.values() if n["active"]]
    return dict(current_user=current_user, CITIES=CITIES, today=today,
                active_notices=active_notices)

@public_bp.route("/")
def index():
    return render_template("index.html")

@public_bp.route("/search")
def search():
    origin      = request.args.get("origin","").strip()
    destination = request.args.get("destination","").strip()
    travel_date = request.args.get("date", date.today().isoformat())
    passengers  = int(request.args.get("passengers", 1))
    today       = date.today().isoformat()
    min_date    = today
    max_date    = (date.today().replace(year=date.today().year+1)).isoformat()
    results = []
    if origin and destination and origin != destination:
        route = next((r for r in ROUTES.values()
                      if r["origin"]==origin and r["destination"]==destination), None)
        if route:
            for sch in SCHEDULES.values():
                if sch["route_id"]==route["id"] and sch["date"]==travel_date:
                    avail = available_seats(sch["id"])
                    if avail >= passengers:
                        # Aplicar bono si el usuario tiene
                        user = current_user()
                        discount = 0.0
                        if user:
                            ub = user_active_bono(user["id"])
                            if ub:
                                from backend.db import BONOS
                                discount = BONOS[ub["bono_id"]]["discount"]
                        base_price = route["price"] * passengers
                        total = round(base_price * (1 - discount), 2)
                        results.append({
                            "schedule": sch,
                            "route": route,
                            "available": avail,
                            "total_price": total,
                            "discount": discount,
                        })
            results.sort(key=lambda x: x["schedule"]["departure"])
    return render_template("search.html",
        origin=origin, destination=destination, travel_date=travel_date,
        passengers=passengers, results=results,
        min_date=min_date, max_date=max_date)

@public_bp.route("/avisos")
def avisos():
    notices = list(NOTICES.values())
    return render_template("avisos.html", notices=notices)

@public_bp.route("/bonos")
def bonos():
    user = current_user()
    my_bonos = USER_BONOS.get(user["id"], []) if user else []
    return render_template("bonos.html", bonos=list(BONOS.values()), my_bonos=my_bonos)
