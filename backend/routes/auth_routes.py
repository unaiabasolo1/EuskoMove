from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from backend.db import SessionLocal, User, _hash, check_password

auth_bp = Blueprint("auth", __name__)

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
    email = request.form.get("email", "").strip().lower()
    pw    = request.form.get("password", "")
    nxt   = request.form.get("next", "") or url_for("public.index")
    db = SessionLocal()
    try:
        user = db.query(User).filter_by(email=email).first()
        
        # 👇 CAMBIO CLAVE: Comprobamos la contraseña usando el verificador robusto de bcrypt
        if not user or not check_password(pw, user.password):
            flash("Email o contraseña incorrectos.", "error")
            return render_template("login.html", next=nxt, email=email)
            
        session["user_id"] = user.id
        flash(f"¡Bienvenido/a, {user.name.split()[0]}!", "success")
    finally:
        db.close()
    return redirect(nxt)

@auth_bp.route("/logout", methods=["POST"])
def logout():
    session.clear()
    flash("Sesión cerrada.", "info")
    return redirect(url_for("public.index"))

@auth_bp.route("/register", methods=["GET"])
def register():
    return render_template("register.html", name="", email="")

@auth_bp.route("/register", methods=["POST"])
def do_register():
    name  = request.form.get("name", "").strip()
    email = request.form.get("email", "").strip().lower()
    pw    = request.form.get("password", "")
    password2   = request.form.get("password2", "") # Ajustado a password2 del HTML original
    
    if not name or not email or not pw:
        flash("Todos los campos son obligatorios.", "error")
        return render_template("register.html", name=name, email=email)
        
    if pw != password2:
        flash("Las contraseñas no coinciden.", "error")
        return render_template("register.html", name=name, email=email)
        
    db = SessionLocal()
    try:
        if db.query(User).filter_by(email=email).first():
            flash("Ese email ya está registrado.", "error")
            return render_template("register.html", name=name, email=email)
            
        # 👇 Al usar _hash(pw), el nuevo db.py creará automáticamente un hash bcrypt seguro
        user = User(name=name, email=email, password=_hash(pw), role="user")
        db.add(user)
        db.commit()
        db.refresh(user)
        session["user_id"] = user.id
        flash("¡Cuenta creada! Bienvenido/a.", "success")
    finally:
        db.close()
    return redirect(url_for("public.index"))