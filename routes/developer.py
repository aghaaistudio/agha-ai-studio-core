from flask import (
    Blueprint, abort, flash, redirect, render_template, request, session, url_for,
)
from flask_login import current_user, login_required
from extensions import db
from models.api import Application, ApiKey

developer_bp = Blueprint("developer", __name__, url_prefix="/developer")

@developer_bp.get("/")
@login_required
def dashboard():
    apps = Application.query.filter_by(user_id=current_user.id).order_by(Application.created_at.desc()).all()
    # Pop the new key so it shows exactly once
    new_key = session.pop("new_api_key", None)
    return render_template("developer/dashboard.html", apps=apps, new_key=new_key)

@developer_bp.post("/apps")
@login_required
def create_app():
    name = (request.form.get("name") or "").strip()
    description = (request.form.get("description") or "").strip()
    if not name:
        flash("Application name is required.", "error")
        return redirect(url_for("developer.dashboard"))
    app_obj = Application(user_id=current_user.id, name=name, description=description)
    db.session.add(app_obj)
    db.session.commit()
    flash(f"Application '{name}' created. You can now generate an API key.", "success")
    return redirect(url_for("developer.dashboard"))

@developer_bp.post("/apps/<int:app_id>/keys")
@login_required
def create_key(app_id):
    app_obj = Application.query.filter_by(id=app_id, user_id=current_user.id).first()
    if not app_obj:
        abort(404)
    key_obj, plain_key = ApiKey.issue(application=app_obj, name="Default Key", scopes="generate")
    db.session.add(key_obj)
    db.session.commit()
    session["new_api_key"] = plain_key
    flash("API key generated. Copy it now — it will not be shown again.", "success")
    return redirect(url_for("developer.dashboard"))

@developer_bp.post("/keys/<int:key_id>/revoke")
@login_required
def revoke_key(key_id):
    key_obj = ApiKey.query.filter_by(id=key_id, user_id=current_user.id).first()
    if not key_obj:
        abort(404)
    key_obj.is_active = False
    db.session.commit()
    flash("API key revoked.", "success")
    return redirect(url_for("developer.dashboard"))
