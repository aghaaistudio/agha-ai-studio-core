from flask import Blueprint, render_template, flash, redirect, url_for, request
from flask_login import current_user, login_required
from extensions import db

user_bp = Blueprint("user", __name__)

@user_bp.get("/settings")
@login_required
def settings():
    return render_template("settings.html")

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
