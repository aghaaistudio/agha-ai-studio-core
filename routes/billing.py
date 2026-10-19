from flask import Blueprint, render_template, flash, redirect, url_for, request
from flask_login import current_user, login_required
from extensions import db
from models.billing import Transaction

billing_bp = Blueprint("billing", __name__, url_prefix="/billing")

@billing_bp.get("/")
@login_required
def index():
    return render_template("billing.html")

@billing_bp.post("/checkout")
@login_required
def checkout():
    method = request.form.get("payment_method")
    package = request.form.get("package")
    
    # Define packages (PKR -> Credits)
    packages = {
        "starter": {"pkr": 500, "credits": 100},
        "pro": {"pkr": 2000, "credits": 500},
        "business": {"pkr": 5000, "credits": 1500}
    }
    
    if package not in packages or not method:
        flash("Invalid package or payment method.", "error")
        return redirect(url_for("billing.index"))
        
    selected = packages[package]
    
    # Create transaction record
    tx = Transaction(
        user_id=current_user.id,
        amount_pkr=selected["pkr"],
        credits_added=selected["credits"],
        payment_method=method,
        status="Completed" # Instant success for testing purposes
    )
    db.session.add(tx)
    
    # Add credits to user
    current_user.credits += selected["credits"]
    db.session.commit()
    
    flash(f"Payment successful via {method}. {selected['credits']} credits added to your account!", "success")
    return redirect(url_for("main.home"))
