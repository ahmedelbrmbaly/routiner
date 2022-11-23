
# import os

from cs50 import SQL
from flask import Flask, flash, redirect,  render_template, request, session, url_for
from flask_session import Session
# from tempfile import mkdtemp
from werkzeug.security import check_password_hash, generate_password_hash

from helper import login_required

from pyisemail import is_email


# Configure application
app = Flask(__name__)

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True



# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///routiner.db")



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

  return render_template("index.html")


@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        
        rows1 = db.execute("SELECT * FROM users WHERE user_name = ?", request.form.get("username"))

        rows2 = db.execute("SELECT * FROM users WHERE email = ?", request.form.get("email"))

        if not request.form.get("username") or len(rows1) != 0:
            flash("Username is not available")
            return redirect(url_for('register'))


        elif not request.form.get("password") or request.form.get("password") != request.form.get("confirmation"):
            flash("Must provide a password and confirm it")
            return redirect(url_for('register'))
        
        
        elif not request.form.get("email") or not is_email(request.form.get("email"), check_dns=True) or len(rows2) != 0:
            flash("Email address is not available")
            return redirect(url_for('register'))

        else:
            db.execute("INSERT INTO users(user_name, password, email) VALUES(?,?,?)", request.form.get("username"), generate_password_hash(request.form.get("password")), request.form.get("email"))

            rows = db.execute("SELECT * FROM users WHERE user_name = ?", request.form.get("username"))

            #  Remember which user has logged in
            session["user_id"] = rows[0]["ID"]

            # Redirect user to home page
            # flash("submitted")
            # return redirect(url_for('register'))  
            return redirect("/")      
    else:
      
        return render_template("register.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        if not request.form.get("username") or not request.form.get("password"):
            flash("Invalid Username and/or Password")
            return redirect(url_for('login'))

        rows = db.execute("SELECT * FROM users WHERE user_name = ?", request.form.get("username"))

        if len(rows) != 1 or not check_password_hash(rows[0]["password"], request.form.get("password")):
            flash("Invalid Username and/or Password")
            return redirect(url_for('login'))

        session["user_id"] = rows[0]["ID"]

        return redirect("/")

        

    else:

        return render_template("login.html")

        

@app.route("/logout")
@login_required
def logout():
    """Log user out"""

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/")

