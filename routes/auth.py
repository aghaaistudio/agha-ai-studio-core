"""
Authentication routes: register, login, logout, forgot password, reset password.
"""
import re
from flask import (
    Blueprint, flash, redirect, render_template, request, url_for, current_app
)
from flask_login import current_user, login_required, login_user, logout_user
from flask_mail import Message

from extensions import db, mail
from models.user import User

auth_bp = Blueprint("auth", __name__)
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
        if len(name) < 2: errors.append("Name must be at least 2 characters.")
        if not _EMAIL_RE.match(email): errors.append("Please enter a valid email address.")
        if len(password) < 8: errors.append("Password must be at least 8 characters.")
        if password != password_confirm: errors.append("Passwords do not match.")

        if not errors:
            existing = User.query.filter_by(email=email).first()
            if existing: errors.append("An account with this email already exists.")

        if errors:
            for msg in errors: flash(msg, "error")
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


@auth_bp.route("/forgot-password", methods=["GET", "POST"])
def forgot_password():
    if current_user.is_authenticated:
        return redirect(url_for("main.home"))

    if request.method == "POST":
        email = (request.form.get("email") or "").strip().lower()
        user = User.query.filter_by(email=email).first()

        if user:
            try:
                token = user.generate_reset_token()
                db.session.commit()
                reset_url = url_for("auth.reset_password", token=token, _external=True)

                try:
                    msg = Message("Password Reset - Agha AI Studio", recipients=[user.email])
                    msg.body = f"To reset your password, visit the following link:\n\n{reset_url}\n\nIf you did not make this request, ignore this email."
                    mail.send(msg)
                    flash("An email has been sent with password reset instructions.", "success")
                except Exception as e:
                    print("\n" + "="*50)
                    print(">>> TEST RESET LINK (Copy this URL):")
                    print(reset_url)
                    print("="*50 + "\n")
                    flash("Email server not configured. Please check the Termux terminal for the reset link.", "error")
            except Exception as e:
                db.session.rollback()
                flash("An error occurred while generating the reset link. Please try again.", "error")

            return redirect(url_for("auth.login"))
        else:
            flash("If an account with that email exists, a reset link has been sent.", "success")
            return redirect(url_for("auth.login"))

    return render_template("auth/forgot_password.html")


@auth_bp.route("/reset-password/<token>", methods=["GET", "POST"])
def reset_password(token):
    if current_user.is_authenticated:
        return redirect(url_for("main.home"))

    user = User.query.filter_by(reset_token=token).first()

    if not user or not user.verify_reset_token(token):
        flash("That is an invalid or expired token.", "error")
        return redirect(url_for("auth.forgot_password"))

    if request.method == "POST":
        password = request.form.get("password") or ""
        password_confirm = request.form.get("password_confirm") or ""

        if len(password) < 8:
            flash("Password must be at least 8 characters.", "error")
        elif password != password_confirm:
            flash("Passwords do not match.", "error")
        else:
            user.set_password(password)
            user.reset_token = None
            user.reset_token_expiry = None
            db.session.commit()
            flash("Your password has been updated! You can now log in.", "success")
            return redirect(url_for("auth.login"))

    return render_template("auth/reset_password.html")
