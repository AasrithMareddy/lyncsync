import os
import time

from cs50 import SQL
from datetime import datetime, timedelta
from flask import Flask, flash, jsonify, redirect, render_template, request, session
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.security import check_password_hash, generate_password_hash
from helpers import apology, login_required

# Configure application
app = Flask(__name__)

app.config["TEMPLATES_AUTO_RELOAD"] = True

app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

db = SQL("sqlite:///lyncsync.db")


@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


def delete_expired_links():
    current_datetime = datetime.now().timestamp()

    # Delete expired links directly from the database
    db.execute("DELETE FROM users_links WHERE expiration_type='temporary' AND (created_at + expiration_time) <= ?", current_datetime)


@app.route("/", methods=["GET", "POST"])
@login_required
def index():
    user_id = session["user_id"]

    if request.method == "POST":
        link = request.form.get("link")
        device = request.form.get("device")
        expiration_type = request.form.get("expiration_type")
        expiration_time_str = request.form.get("expiration_time")
        expiration_unit = request.form.get("expiration-unit")
        current_datetime = datetime.now()
        created_at = current_datetime.timestamp()

        # Check if expiration_time_str is not None
        expiration_time = int(expiration_time_str) if expiration_time_str is not None else 0

        # Convert expiration time to seconds
        if expiration_type == "temporary":
            if expiration_unit == "minutes":
                expiration_time *= 60
            elif expiration_unit == "hours":
                expiration_time *= 3600
            elif expiration_unit == "days":
                expiration_time *= 86400

        # Add data to db, associating it with the logged-in user
        db.execute("INSERT INTO users_links (links, devices, user_id, expiration_type, expiration_time, created_at) VALUES (?, ?, ?, ?, ?, ?)",
                   link, device, user_id, expiration_type, expiration_time, created_at)
        return redirect("/")
        time.sleep(expiration_time)
        delete_expired_links()

    else:
        delete_expired_links()
        # Display the entries in the database for the logged-in user on index.html
        links = db.execute("SELECT * FROM users_links WHERE user_id = ?", user_id)

        return render_template("index.html", links=links)


@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""

    # Forget any user_id
    session.clear()

    if request.method == "POST":
        # Ensure username was submitted
        if not request.form.get("username"):
            return apology("must provide username", 403)

        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password", 403)

        # Query database for username
        rows = db.execute(
            "SELECT * FROM users WHERE username = ?", (request.form.get("username"))
        )

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(
            rows[0]["hash"], request.form.get("password")
        ):
            return apology("invalid username and/or password", 403)

        # Remember which user has logged in
        session["user_id"] = rows[0]["id"]

        # Redirect user to home page
        return redirect("/")

    else:
        return render_template("login.html")


@app.route("/logout")
def logout():
    """Log user out"""

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/")


@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        confirmation = request.form.get("confirmation")

        # Ensure username was submitted
        if not username:
            return apology("must provide username")

        # Ensure password was submitted
        elif not password:
            return apology("must provide password")

        elif not confirmation:
            return apology("must provide password confirmation")

        if password != confirmation:
            return apology("password confirmation does not match")

        # Check if username already in database
        rows = db.execute("SELECT * FROM users WHERE username = ?", username)
        if len(rows) > 0:
            return apology("Username already exists")

        # Hash the password
        hash_password = generate_password_hash(password)

        # Save new user with username
        db.execute(
            "INSERT INTO users (username, hash) VALUES (?, ?)", username, hash_password
        )

        # Log the user in (optional)
        # Retrieve the user_id for the newly registered user
        user_id = db.execute("SELECT id FROM users WHERE username = ?", username)[0]["id"]
        session["user_id"] = user_id

        return redirect("/")

    else:
        return render_template("registration.html")
