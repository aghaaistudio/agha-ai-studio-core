from flask import Blueprint, render_template, flash, redirect, url_for, request
from flask_login import current_user, login_required
from extensions import db
from models.usage import UsageRecord

user_bp = Blueprint("user", __name__)

@user_bp.get("/settings")
@login_required
def settings():
    # Fetch user's recent usage history
    usages = UsageRecord.query.filter_by(user_id=current_user.id).order_by(UsageRecord.created_at.desc()).limit(20).all()
    return render_template("settings.html", usages=usages)

@user_bp.post("/change-password")
@login_required
def change_password():
    current_pwd = request.form.get("current_password")
    new_pwd = request.form.get("new_password")

    if not current_user.check_password(current_pwd):
        flash("Incorrect current password.", "error")
        return redirect(url_for("user.settings"))

    if len(new_pwd) < 8:
        flash("New password must be at least 8 characters.", "error")
        return redirect(url_for("user.settings"))

    current_user.set_password(new_pwd)
    db.session.commit()
    flash("Password updated successfully!", "success")
    return redirect(url_for("user.settings"))

@user_bp.post("/update-name")
@login_required
def update_name():
    new_name = request.form.get("name", "").strip()
    if len(new_name) < 2:
        flash("Name must be at least 2 characters.", "error")
    else:
        current_user.name = new_name
        db.session.commit()
        flash("Name updated successfully!", "success")
    return redirect(url_for("user.settings"))
