"""Local-only Flask login application with secure defaults."""
import os
import secrets
import sqlite3
from pathlib import Path

from flask import Flask, flash, redirect, render_template, request, session, url_for
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from flask_wtf.csrf import CSRFProtect
from werkzeug.security import check_password_hash, generate_password_hash

from database import create_user, get_user_by_username, initialize_database

csrf = CSRFProtect()
limiter = Limiter(key_func=get_remote_address, default_limits=[])


def create_app(test_config=None):
    app = Flask(__name__)
    instance_dir = Path(app.instance_path)
    instance_dir.mkdir(parents=True, exist_ok=True)
    app.config.from_mapping(
        SECRET_KEY=os.environ.get("SECRET_KEY") or secrets.token_hex(32),
        DATABASE=os.environ.get("DATABASE_PATH", str(instance_dir / "users.sqlite3")),
        SESSION_COOKIE_HTTPONLY=True,
        SESSION_COOKIE_SAMESITE="Lax",
        SESSION_COOKIE_SECURE=os.environ.get("COOKIE_SECURE", "false").lower() == "true",
        MAX_CONTENT_LENGTH=16 * 1024,
        RATELIMIT_STORAGE_URI=os.environ.get("RATELIMIT_STORAGE_URI", "memory://"),
        RATELIMIT_HEADERS_ENABLED=True,
    )
    if test_config:
        app.config.update(test_config)
    csrf.init_app(app)
    limiter.init_app(app)
    initialize_database(app.config["DATABASE"])

    @app.get("/")
    def index():
        return redirect(url_for("dashboard" if session.get("user_id") else "login"))

    @app.route("/register", methods=["GET", "POST"])
    def register():
        if request.method == "POST":
            username = request.form.get("username", "").strip()
            password = request.form.get("password", "")
            if not valid_username(username) or not valid_password(password):
                flash("Use a 3-30 character username (letters, numbers, underscore) and a password of at least 12 characters.", "error")
                return render_template("register.html"), 400
            if get_user_by_username(app.config["DATABASE"], username):
                flash("That username is unavailable.", "error")
                return render_template("register.html"), 409
            try:
                create_user(app.config["DATABASE"], username, generate_password_hash(password))
            except sqlite3.IntegrityError:
                flash("That username is unavailable.", "error")
                return render_template("register.html"), 409
            flash("Account created. You can now sign in.", "success")
            return redirect(url_for("login"))
        return render_template("register.html")

    @app.route("/login", methods=["GET", "POST"])
    @limiter.limit("5 per minute", methods=["POST"])
    def login():
        if request.method == "POST":
            username = request.form.get("username", "").strip()
            password = request.form.get("password", "")
            user = get_user_by_username(app.config["DATABASE"], username) if valid_username(username) else None
            if user is None or not check_password_hash(user["password_hash"], password):
                flash("Invalid username or password.", "error")
                return render_template("login.html"), 401
            session.clear()
            session["user_id"] = user["id"]
            session["username"] = user["username"]
            return redirect(url_for("dashboard"))
        return render_template("login.html")

    @app.get("/dashboard")
    def dashboard():
        if not session.get("user_id"):
            return redirect(url_for("login"))
        return render_template("dashboard.html", username=session.get("username", "user"))

    @app.post("/logout")
    def logout():
        session.clear()
        flash("You have been signed out.", "success")
        return redirect(url_for("login"))

    @app.errorhandler(413)
    def request_too_large(_error):
        return "Request too large.", 413

    @app.errorhandler(500)
    def internal_error(_error):
        app.logger.exception("Unexpected application error")
        return "An internal error occurred.", 500

    return app


def valid_username(username):
    return (
        username.isascii()
        and 3 <= len(username) <= 30
        and all(char.isalnum() or char == "_" for char in username)
    )


def valid_password(password):
    return 12 <= len(password) <= 128


if __name__ == "__main__":
    create_app().run(host="127.0.0.1", port=5000, debug=False)
