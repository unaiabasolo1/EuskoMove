import re
import logging
from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from backend.db import SessionLocal, User, _hash, check_password

auth_bp = Blueprint("auth", __name__)

# Logger propio de este módulo (hereda la config definida en app.py)
logger = logging.getLogger("euskomove.auth")

# ─── Reglas de validación (basadas en recomendaciones NIST) ──────────────────

# Email con formato razonable (usuario@dominio.com)
EMAIL_RE = re.compile(r"^[A-Za-z0-9._%+\-]+@[A-Za-z0-9.\-]+\.[A-Za-z]{2,}$")

# Nombre: letras (incluye acentos y ñ), números, espacios y - _ .
NAME_RE = re.compile(r"^[A-Za-zÀ-ÿ0-9 ._\-]+$")

# Longitudes
NAME_MIN, NAME_MAX = 3, 30
PW_MIN, PW_MAX = 8, 64

# Nombres reservados que no se permiten registrar
NOMBRES_RESERVADOS = {"admin", "root", "support", "administrator", "superuser", "system"}

# Contraseñas más comunes / comprometidas (lista corta; ampliable)
PASSWORDS_COMUNES = {
    "12345678", "123456789", "1234567890", "password", "password1", "passw0rd",
    "qwerty123", "11111111", "00000000", "abc12345", "iloveyou", "admin123",
    "welcome1", "contraseña", "12341234", "1q2w3e4r", "987654321", "qwertyuiop",
}


def validar_registro(name: str, email: str, pw: str, password2: str):
    """Devuelve un mensaje de error si algo no es válido, o None si todo está bien."""

    # ── Campos obligatorios ──
    if not name or not email or not pw:
        return "Todos los campos son obligatorios."

    # ── Nombre ──
    if len(name) < NAME_MIN or len(name) > NAME_MAX:
        return f"El nombre debe tener entre {NAME_MIN} y {NAME_MAX} caracteres."
    if not NAME_RE.match(name):
        return "El nombre solo puede contener letras, números, espacios y los símbolos . _ -"
    if name.isdigit():
        return "El nombre no puede ser solo números."
    if name.strip().lower() in NOMBRES_RESERVADOS:
        return "Ese nombre está reservado y no se puede usar."

    # ── Email ──
    if not EMAIL_RE.match(email):
        return "Introduce un email válido (por ejemplo: nombre@dominio.com)."

    # ── Contraseña ──
    # Longitud: mínimo 8, permitir frases largas (hasta 64).
    # No se obligan símbolos/mayúsculas (recomendación NIST).
    if len(pw) < PW_MIN:
        return f"La contraseña debe tener al menos {PW_MIN} caracteres."
    if len(pw) > PW_MAX:
        return f"La contraseña no puede superar los {PW_MAX} caracteres."
    if pw.lower() in PASSWORDS_COMUNES:
        return "Esa contraseña es demasiado común. Elige una más segura."

    # ── Confirmación ──
    if pw != password2:
        return "Las contraseñas no coinciden."

    return None


def current_user():
    uid = session.get("user_id")
    if not uid:
        return None
    db = SessionLocal()
    try:
        return db.query(User).get(uid)
    finally:
        db.close()

@auth_bp.route("/login", methods=["GET"])
def login():
    return render_template("login.html", next=request.args.get("next", ""), email="")

@auth_bp.route("/login", methods=["POST"])
def do_login():
    logger.debug("Procesando intento de login (formulario recibido)")
    email = request.form.get("email", "").strip().lower()
    pw    = request.form.get("password", "")
    nxt   = request.form.get("next", "") or url_for("public.index")
    db = SessionLocal()
    try:
        user = db.query(User).filter_by(email=email).first()

        if not user or not check_password(pw, user.password):
            logger.warning("Intento de login fallido para el email: %s", email)
            flash("Email o contraseña incorrectos.", "error")
            return render_template("login.html", next=nxt, email=email)

        session["user_id"] = user.id
        logger.info("Login correcto: usuario id=%s (%s)", user.id, email)
        flash(f"¡Bienvenido/a, {user.name.split()[0]}!", "success")
    except Exception as e:
        logger.error("Error inesperado durante el login de %s: %s", email, e)
        raise
    finally:
        db.close()
    return redirect(nxt)

@auth_bp.route("/logout", methods=["POST"])
def logout():
    uid = session.get("user_id")
    session.clear()
    logger.info("Sesión cerrada para usuario id=%s", uid)
    flash("Sesión cerrada.", "info")
    return redirect(url_for("public.index"))

@auth_bp.route("/register", methods=["GET"])
def register():
    return render_template("register.html", name="", email="")

@auth_bp.route("/register", methods=["POST"])
def do_register():
    logger.debug("Procesando intento de registro (formulario recibido)")
    name  = request.form.get("name", "").strip()
    email = request.form.get("email", "").strip().lower()
    pw    = request.form.get("password", "")
    password2   = request.form.get("password2", "") # Ajustado a password2 del HTML original

    # ─── Validación de seguridad de los datos introducidos ───
    error = validar_registro(name, email, pw, password2)
    if error:
        logger.warning("Registro rechazado (%s) para email=%s, name=%s", error, email, name)
        flash(error, "error")
        return render_template("register.html", name=name, email=email)

    db = SessionLocal()
    try:
        # Evitar cuentas duplicadas con el mismo email
        if db.query(User).filter_by(email=email).first():
            logger.warning("Registro rechazado: email duplicado (%s)", email)
            flash("Ese email ya está registrado.", "error")
            return render_template("register.html", name=name, email=email)

        # Evitar nombres duplicados (case-insensitive)
        if db.query(User).filter(User.name.ilike(name)).first():
            logger.warning("Registro rechazado: nombre duplicado (%s)", name)
            flash("Ese nombre ya está en uso. Elige otro.", "error")
            return render_template("register.html", name=name, email=email)

        user = User(name=name, email=email, password=_hash(pw), role="user")
        db.add(user)
        db.commit()
        db.refresh(user)
        session["user_id"] = user.id
        logger.info("Nuevo usuario registrado: id=%s, email=%s", user.id, email)
        flash("¡Cuenta creada! Bienvenido/a.", "success")
    except Exception as e:
        logger.error("Error inesperado durante el registro de %s: %s", email, e)
        raise
    finally:
        db.close()
    return redirect(url_for("public.index"))