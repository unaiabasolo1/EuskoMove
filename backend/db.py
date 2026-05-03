
"""db.py — almacén de datos en memoria."""
import hashlib, uuid
from datetime import date, timedelta

def _hash(pw): return hashlib.sha256(pw.encode()).hexdigest()

def _make_schedules():
    s, sid, today = {}, 1, date.today()
    times = {
        1:["07:00","08:30","10:00","11:30","13:00","14:30","16:00","17:30","19:00","20:30"],
        2:["07:30","09:00","10:30","12:00","13:30","15:00","16:30","18:00","19:30","21:00"],
        3:["07:15","09:15","11:15","13:15","15:15","17:15","19:15","21:15"],
        4:["08:00","10:00","12:00","14:00","16:00","18:00","20:00","22:00"],
        5:["08:00","10:00","12:00","14:00","16:30","18:30","20:30"],
        6:["08:45","10:45","12:45","14:45","17:15","19:15","21:15"],
    }
    for offset in range(14):
        d = today + timedelta(days=offset)
        for rid, tlist in times.items():
            for t in tlist:
                s[sid] = {"id":sid,"route_id":rid,"date":d.isoformat(),
                          "departure":t,"bus_code":f"EM{rid:02d}{sid:05d}"[-7:],"capacity":50}
                sid += 1
    return s

ROUTES = {
    1:{"id":1,"origin":"Vitoria-Gasteiz","destination":"Bilbao",          "duration":"50 min",   "price":4.90},
    2:{"id":2,"origin":"Bilbao",          "destination":"Vitoria-Gasteiz","duration":"50 min",   "price":4.90},
    3:{"id":3,"origin":"Vitoria-Gasteiz","destination":"Donostia-S.S.",   "duration":"1h 15 min","price":7.50},
    4:{"id":4,"origin":"Donostia-S.S.",  "destination":"Vitoria-Gasteiz","duration":"1h 15 min","price":7.50},
    5:{"id":5,"origin":"Bilbao",          "destination":"Donostia-S.S.",  "duration":"1h 20 min","price":6.50},
    6:{"id":6,"origin":"Donostia-S.S.",  "destination":"Bilbao",          "duration":"1h 20 min","price":6.50},
}
SCHEDULES = _make_schedules()

USERS = {
    1:{"id":1,"name":"Admin EuskoMove","email":"admin@euskomove.eus","password":_hash("admin123"),"role":"admin"},
    2:{"id":2,"name":"Ane Etxebarria", "email":"ane@euskomove.eus", "password":_hash("user123"), "role":"user"},
}

RESERVATIONS = {}
CITIES = ["Vitoria-Gasteiz","Bilbao","Donostia-S.S."]

# Avisos de incidencias
NOTICES = {
    1:{"id":1,"type":"info",   "title":"Cambio de horario","text":"El servicio Bilbao→Donostia de las 08:00 h sale a las 08:15 h los lunes.","active":True},
    2:{"id":2,"type":"warning","title":"Obras en A-1",      "text":"Posibles retrasos de 10-15 min en la ruta Vitoria↔Bilbao por obras en la A-1.","active":True},
    3:{"id":3,"type":"info",   "title":"Servicio especial","text":"Se añaden refuerzos los viernes por la tarde en todas las rutas.","active":True},
}

# Bonos de transporte
BONOS = {
    1:{"id":1,"name":"Bono 10",    "trips":10,"discount":0.20,"price":39.20, "desc":"10 viajes con 20% de descuento"},
    2:{"id":2,"name":"Bono Joven", "trips":10,"discount":0.30,"price":34.30, "desc":"Para menores de 26 años · 30% de descuento"},
    3:{"id":3,"name":"Bono Mensual","trips":30,"discount":0.35,"price":95.55,"desc":"30 viajes al mes con 35% de descuento"},
}

USER_BONOS = {}   # {user_id: [{bono_id, trips_left, purchased_at}]}

_c = {"uid":3,"rid":1,"nid":4,"bid":1}

def next_uid():
    v=_c["uid"]; _c["uid"]+=1; return v
def next_rid():
    v=_c["rid"]; _c["rid"]+=1; return v
def next_nid():
    v=_c["nid"]; _c["nid"]+=1; return v

def get_booked_seats(schedule_id):
    return {r["seat"] for r in RESERVATIONS.values() if r["schedule_id"]==schedule_id}

def available_seats(schedule_id):
    s = SCHEDULES.get(schedule_id)
    return 0 if not s else s["capacity"] - len(get_booked_seats(schedule_id))

def make_locator():
    return uuid.uuid4().hex[:8].upper()

def user_active_bono(user_id):
    """Devuelve el primer bono con viajes disponibles del usuario, o None."""
    for ub in USER_BONOS.get(user_id, []):
        if ub["trips_left"] > 0:
            return ub
    return None

def use_bono_trip(user_id):
    """Descuenta un viaje del bono activo. Devuelve el % de descuento o 0."""
    ub = user_active_bono(user_id)
    if ub:
        bono = BONOS[ub["bono_id"]]
        ub["trips_left"] -= 1
        return bono["discount"]
    return 0.0
