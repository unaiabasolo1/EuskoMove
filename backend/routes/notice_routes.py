from flask import Blueprint, request, redirect, url_for, flash, session
from backend.db import SessionLocal, Notice

notice_bp = Blueprint("notice", __name__)

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

def admin_required():
    u = current_user()
    return u and u.role == "admin"

@notice_bp.route("/admin/notice/add", methods=["POST"])
def add_notice():
    if not admin_required():
        flash("Acceso denegado.", "error")
        return redirect(url_for("public.index"))
    title = request.form.get("title", "").strip()
    text  = request.form.get("text", "").strip()
    ntype = request.form.get("type", "info")
    if title and text:
        db = SessionLocal()
        try:
            db.add(Notice(type=ntype, title=title, text=text, active=True))
            db.commit()
            flash("Aviso publicado.", "success")
        finally:
            db.close()
    return redirect(url_for("admin.admin"))

@notice_bp.route("/admin/notice/<int:nid>/toggle", methods=["POST"])
def toggle_notice(nid):
    if not admin_required():
        return redirect(url_for("public.index"))
    db = SessionLocal()
    try:
        n = db.query(Notice).get(nid)
        if n:
            n.active = not n.active
            db.commit()
    finally:
        db.close()
    return redirect(url_for("admin.admin"))

@notice_bp.route("/admin/notice/<int:nid>/delete", methods=["POST"])
def delete_notice(nid):
    if not admin_required():
        return redirect(url_for("public.index"))
    db = SessionLocal()
    try:
        n = db.query(Notice).get(nid)
        if n:
            db.delete(n)
            db.commit()
    finally:
        db.close()
    return redirect(url_for("admin.admin"))