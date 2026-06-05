"""db.py — acceso a datos con SQLAlchemy + PostgreSQL."""
import os, uuid
import bcrypt
from datetime import date, timedelta
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker, DeclarativeBase, Session
from sqlalchemy import Column, Integer, String, Float, Boolean, Date, ForeignKey
from sqlalchemy.orm import relationship

DATABASE_URL = os.environ.get("DATABASE_URL", "sqlite:///euskomove.db")

engine = create_engine(DATABASE_URL, pool_pre_ping=True)
SessionLocal = sessionmaker(bind=engine)


def get_db() -> Session:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# ─── NUEVAS FUNCIONES DE SEGURIDAD CON BCRYPT ─────────────────────────────────

def _hash(pw: str) -> str:
    """Genera un hash bcrypt seguro con salt automático y factor de coste 12."""
    salt = bcrypt.gensalt(rounds=12)
    hash_bytes = bcrypt.hashpw(pw.encode('utf-8'), salt)
    return hash_bytes.decode('utf-8')

def check_password(password_plana: str, hash_guardado: str) -> bool:
    """Verifica de forma segura si la contraseña introducida coincide con el hash."""
    if not password_plana or not hash_guardado:
        return False
    return bcrypt.checkpw(password_plana.encode('utf-8'), hash_guardado.encode('utf-8'))

def make_locator(): return uuid.uuid4().hex[:8].upper()


# ─── Modelos ──────────────────────────────────────────────────────────────────

class Base(DeclarativeBase):
    pass


class User(Base):
    __tablename__ = "users"
    id       = Column(Integer, primary_key=True)
    name     = Column(String(120), nullable=False)
    email    = Column(String(120), unique=True, nullable=False)
    password = Column(String(64), nullable=False)
    role     = Column(String(20), default="user")
    reservations = relationship("Reservation", back_populates="user")
    bonos        = relationship("UserBono", back_populates="user")


class Route(Base):
    __tablename__ = "routes"
    id          = Column(Integer, primary_key=True)
    origin      = Column(String(80), nullable=False)
    destination = Column(String(80), nullable=False)
    duration    = Column(String(20))
    price       = Column(Float)
    schedules   = relationship("Schedule", back_populates="route")


class Schedule(Base):
    __tablename__ = "schedules"
    id        = Column(Integer, primary_key=True)
    route_id  = Column(Integer, ForeignKey("routes.id"))
    date      = Column(String(10))
    departure = Column(String(5))
    bus_code  = Column(String(20))
    capacity  = Column(Integer, default=50)
    route        = relationship("Route", back_populates="schedules")
    reservations = relationship("Reservation", back_populates="schedule")


class Reservation(Base):
    __tablename__ = "reservations"
    id                = Column(Integer, primary_key=True)
    user_id          = Column(Integer, ForeignKey("users.id"))
    schedule_id      = Column(Integer, ForeignKey("schedules.id"))
    seat             = Column(String(5))
    locator          = Column(String(8))
    price_paid       = Column(Float)
    discount_applied = Column(Float, default=0.0)
    user     = relationship("User", back_populates="reservations")
    schedule = relationship("Schedule", back_populates="reservations")


class Notice(Base):
    __tablename__ = "notices"
    id     = Column(Integer, primary_key=True)
    type   = Column(String(20))
    title  = Column(String(120))
    text   = Column(String(500))
    active = Column(Boolean, default=True)


class Bono(Base):
    __tablename__ = "bonos"
    id       = Column(Integer, primary_key=True)
    name     = Column(String(80))
    trips    = Column(Integer)
    discount = Column(Float)
    price    = Column(Float)
    desc     = Column(String(200))
    users    = relationship("UserBono", back_populates="bono")


class UserBono(Base):
    __tablename__ = "user_bonos"
    id         = Column(Integer, primary_key=True)
    user_id    = Column(Integer, ForeignKey("users.id"))
    bono_id    = Column(Integer, ForeignKey("bonos.id"))
    trips_left = Column(Integer)
    purchased_at = Column(String(10))
    user = relationship("User", back_populates="bonos")
    bono = relationship("Bono", back_populates="users")


# ─── Inicialización ───────────────────────────────────────────────────────────

def init_db():
    """Crea tablas y rellena datos iniciales si la BD está vacía."""
    Base.metadata.create_all(engine)
    db = SessionLocal()
    try:
        if db.query(User).count() == 0:
            _seed(db)
    finally:
        db.close()


def _seed(db: Session):
    # Usuarios — contraseñas leídas desde Key Vault vía variables de entorno
    db.add_all([
        User(id=1, name="Admin EuskoMove", email="admin@euskomove.eus",
             password=_hash(os.environ.get("ADMIN_PASSWORD", "changeme")), role="admin"),
        User(id=2, name="Ane Etxebarria", email="ane@euskomove.eus",
             password=_hash(os.environ.get("USER_PASSWORD", "changeme")), role="user"),
    ])

    # Rutas
    routes_data = [
        (1, "Vitoria-Gasteiz", "Bilbao",           "50 min",    4.90),
        (2, "Bilbao",           "Vitoria-Gasteiz",  "50 min",    4.90),
        (3, "Vitoria-Gasteiz", "Donostia-S.S.",    "1h 15 min", 7.50),
        (4, "Donostia-S.S.",   "Vitoria-Gasteiz",  "1h 15 min", 7.50),
        (5, "Bilbao",           "Donostia-S.S.",    "1h 20 min", 6.50),
        (6, "Donostia-S.S.",   "Bilbao",            "1h 20 min", 6.50),
    ]
    for rid, org, dst, dur, price in routes_data:
        db.add(Route(id=rid, origin=org, destination=dst, duration=dur, price=price))

    # Horarios (14 días)
    times = {
        1: ["07:00","08:30","10:00","11:30","13:00","14:30","16:00","17:30","19:00","20:30"],
        2: ["07:30","09:00","10:30","12:00","13:30","15:00","16:30","18:00","19:30","21:00"],
        3: ["07:15","09:15","11:15","13:15","15:15","17:15","19:15","21:15"],
        4: ["08:00","10:00","12:00","14:00","16:00","18:00","20:00","22:00"],
        5: ["08:00","10:00","12:00","14:00","16:30","18:30","20:30"],
        6: ["08:45","10:45","12:45","14:45","17:15","19:15","21:15"],
    }
    sid = 1
    today = date.today()
    for offset in range(14):
        d = today + timedelta(days=offset)
        for rid, tlist in times.items():
            for t in tlist:
                db.add(Schedule(
                    id=sid, route_id=rid, date=d.isoformat(),
                    departure=t, bus_code=f"EM{rid:02d}{sid:05d}"[-7:], capacity=50
                ))
                sid += 1

    # Avisos
    db.add_all([
        Notice(id=1, type="info",    title="Cambio de horario",
               text="El servicio Bilbao→Donostia de las 08:00 h sale a las 08:15 h los lunes.", active=True),
        Notice(id=2, type="warning", title="Obras en A-1",
               text="Posibles retrasos de 10-15 min en la ruta Vitoria↔Bilbao por obras en la A-1.", active=True),
        Notice(id=3, type="info",    title="Servicio especial",
               text="Se añaden refuerzos los viernes por la tarde en todas las rutas.", active=True),
    ])

    # Bonos
    db.add_all([
        Bono(id=1, name="Bono 10",     trips=10, discount=0.20, price=39.20,
             desc="10 viajes con 20% de descuento"),
        Bono(id=2, name="Bono Joven",  trips=10, discount=0.30, price=34.30,
             desc="Para menores de 26 años · 30% de descuento"),
        Bono(id=3, name="Bono Mensual",trips=30, discount=0.35, price=95.55,
             desc="30 viajes al mes con 35% de descuento"),
    ])

    db.commit()


# ─── Funciones de ayuda (misma interfaz que antes) ───────────────────────────

def get_booked_seats(schedule_id: int) -> set:
    db = SessionLocal()
    try:
        rows = db.query(Reservation.seat).filter_by(schedule_id=schedule_id).all()
        return {r.seat for r in rows}
    finally:
        db.close()


def available_seats(schedule_id: int) -> int:
    db = SessionLocal()
    try:
        sch = db.query(Schedule).get(schedule_id)
        return 0 if not sch else sch.capacity - len(get_booked_seats(schedule_id))
    finally:
        db.close()


def user_active_bono(user_id: int):
    db = SessionLocal()
    try:
        ub = db.query(UserBono).filter(
            UserBono.user_id == user_id,
            UserBono.trips_left > 0
        ).first()
        if ub:
            return {"bono_id": ub.bono_id, "trips_left": ub.trips_left}
        return None
    finally:
        db.close()


def use_bono_trip(user_id: int) -> float:
    db = SessionLocal()
    try:
        ub = db.query(UserBono).filter(
            UserBono.user_id == user_id,
            UserBono.trips_left > 0
        ).first()
        if ub:
            bono = db.query(Bono).get(ub.bono_id)
            ub.trips_left -= 1
            db.commit()
            return bono.discount
        return 0.0
    finally:
        db.close()