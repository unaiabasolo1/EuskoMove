import hashlib
from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from backend.db import USERS, next_uid, _hash

auth_bp = Blueprint("auth", __name__)

def current_user():
    uid = session.get("user_id")
    return USERS.get(uid)

@auth_bp.route("/login", methods=["GET"])
def login():
    return render_template("login.html", next=request.args.get("next",""), email="")

@auth_bp.route("/login", methods=["POST"])
def do_login():
    email = request.form.get("email","").strip().lower()
    pw    = request.form.get("password","")
    nxt   = request.form.get("next","") or url_for("public.index")
    user  = next((u for u in USERS.values() if u["email"]==email), None)
    if not user or user["password"] != _hash(pw):
        flash("Email o contraseña incorrectos.", "error")
        return render_template("login.html", next=nxt, email=email)
    session["user_id"] = user["id"]
    flash(f"¡Bienvenido/a, {user['name'].split()[0]}!", "success")
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
    name  = request.form.get("name","").strip()
    email = request.form.get("email","").strip().lower()
    pw    = request.form.get("password","")
    pw2   = request.form.get("password2","")
    if not name or not email or not pw:
        flash("Todos los campos son obligatorios.", "error")
        return render_template("register.html", name=name, email=email)
    if pw != pw2:
        flash("Las contraseñas no coinciden.", "error")
        return render_template("register.html", name=name, email=email)
    if any(u["email"]==email for u in USERS.values()):
        flash("Ese email ya está registrado.", "error")
        return render_template("register.html", name=name, email=email)
    uid = next_uid()
    USERS[uid] = {"id":uid,"name":name,"email":email,"password":_hash(pw),"role":"user"}
    session["user_id"] = uid
    flash("¡Cuenta creada! Bienvenido/a.", "success")
    return redirect(url_for("public.index"))
