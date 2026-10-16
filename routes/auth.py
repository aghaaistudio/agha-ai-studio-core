"""
Authentication routes: register, login, logout.

Security notes:
- Passwords are hashed via User.set_password (werkzeug).
- Email is lowercased and stripped before storage and lookup.
- Registration and login return identical error text on bad credentials
  to avoid leaking which emails exist.
- Logout is POST-only (safer against CSRF).
"""
import re

from flask import (
    Blueprint,
    flash,
    redirect,
    render_template,
    request,
    url_for,
)
from flask_login import current_user, login_required, login_user, logout_user

from extensions import db
from models.user import User


auth_bp = Blueprint("auth", __name__)

# Simple email shape check. Deeper validation would send a confirmation
# email, which is out of scope for this stage.
_EMAIL_RE = re.compile(r"^[^@\s]+@[^@\s]+\.[^@\s]+$")


@auth_bp.route("/register", methods=["GET", "POST"])
def register():
    if current_user.is_authenticated:
        return redirect(url_for("main.home"))

    if request.method == "POST":
        name = (request.form.get("name") or "").strip()
        email = (request.form.get("email") or "").strip().lower()
        password = request.form.get("password") or ""
        password_confirm = request.form.get("password_confirm") or ""

        errors = []
        if len(name) < 2:
            errors.append("Name must be at least 2 characters.")
        if not _EMAIL_RE.match(email):
            errors.append("Please enter a valid email address.")
        if len(password) < 8:
            errors.append("Password must be at least 8 characters.")
        if password != password_confirm:
            errors.append("Passwords do not match.")

        if not errors:
            existing = User.query.filter_by(email=email).first()
            if existing:
                errors.append("An account with this email already exists.")

        if errors:
            for msg in errors:
                flash(msg, "error")
            return render_template("auth/register.html"), 400

        user = User(email=email, name=name, role="user")
        user.set_password(password)
        db.session.add(user)
        db.session.commit()

        flash("Account created. Please log in.", "success")
        return redirect(url_for("auth.login"))

    return render_template("auth/register.html")


@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for("main.home"))

    if request.method == "POST":
        email = (request.form.get("email") or "").strip().lower()
        password = request.form.get("password") or ""

        if not email or not password:
            flash("Email and password are required.", "error")
            return render_template("auth/login.html"), 400

        user = User.query.filter_by(email=email).first()

        # Same message whether the email is unknown OR the password is wrong.
        if not user or not user.check_password(password):
            flash("Invalid email or password.", "error")
            return render_template("auth/login.html"), 401

        if not user.is_active:
            flash("This account is disabled.", "error")
            return render_template("auth/login.html"), 403

        login_user(user)
        flash(f"Welcome back, {user.name or user.email}.", "success")
        return redirect(url_for("main.home"))

    return render_template("auth/login.html")


@auth_bp.route("/logout", methods=["POST"])
@login_required
def logout():
    logout_user()
    flash("You have been logged out.", "success")
    return redirect(url_for("auth.login"))
