from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from backend.db import NOTICES, next_nid

notice_bp = Blueprint("notice", __name__)

def current_user():
    from backend.db import USERS
    uid = session.get("user_id")
    return USERS.get(uid)

def admin_required():
    u = current_user()
    return u and u.get("role") == "admin"

@notice_bp.route("/admin/notice/add", methods=["POST"])
def add_notice():
    if not admin_required():
        flash("Acceso denegado.", "error")
        return redirect(url_for("public.index"))
    nid   = next_nid()
    title = request.form.get("title","").strip()
    text  = request.form.get("text","").strip()
    ntype = request.form.get("type","info")
    if title and text:
        NOTICES[nid] = {"id":nid,"type":ntype,"title":title,"text":text,"active":True}
        flash("Aviso publicado.", "success")
    return redirect(url_for("admin.admin"))

@notice_bp.route("/admin/notice/<int:nid>/toggle", methods=["POST"])
def toggle_notice(nid):
    if not admin_required():
        return redirect(url_for("public.index"))
    n = NOTICES.get(nid)
    if n:
        n["active"] = not n["active"]
    return redirect(url_for("admin.admin"))

@notice_bp.route("/admin/notice/<int:nid>/delete", methods=["POST"])
def delete_notice(nid):
    if not admin_required():
        return redirect(url_for("public.index"))
    NOTICES.pop(nid, None)
    return redirect(url_for("admin.admin"))
