
# import os

from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
# from tempfile import mkdtemp
from werkzeug.security import check_password_hash, generate_password_hash

from helper import login_required

# Configure application
app = Flask(__name__)

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True



# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
# db = SQL("sqlite:///finance.db")



@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response

@app.route("/")
@login_required
def index():

  return render_template("layout.html")



@app.route("/logout")
@login_required
def logout():
    """Log user out"""

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/")



@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":

        # rows = db.execute("SELECT * FROM users WHERE username = ?", request.form.get("username"))

        # if not request.form.get("username") or len(rows) == 1:
        #     return apology("Username is not available", 400)


        # elif not request.form.get("password") or request.form.get("password") != request.form.get("confirmation"):
        #     return apology("must provide password and confirm it" , 400)
        # else:
        #     db.execute("INSERT INTO users(username, hash) VALUES(?,?)",
        #                 request.form.get("username"), generate_password_hash(request.form.get("username")))

        #     rows = db.execute("SELECT * FROM users WHERE username = ?", request.form.get("username"))

        #      # Remember which user has logged in
        #     session["user_id"] = rows[0]["id"]

        # Redirect user to home page
            return redirect("/")

        # Ensure username exists and password is correct
    else:
        return render_template("register.html")
