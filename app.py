
# import os

from cs50 import SQL
from flask import Flask, flash, redirect,  render_template, request, session, url_for
from flask_session import Session
# from tempfile import mkdtemp
from werkzeug.security import check_password_hash, generate_password_hash

from helper import login_required

from pyisemail import is_email

from datetime import datetime


import calendar



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


#set firstweekday=0
cal= calendar.Calendar(firstweekday=5)


@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


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
        session["user_name"] = rows[0]["user_name"]
        

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



@app.route("/profile", methods=["GET", "POST"])
@login_required
def profile():
    rows = db.execute("SELECT * FROM users WHERE ID = ?", session["user_id"])
    row= rows[0]
    newRow = rows[0]

    if request.method == "POST":

        
        if request.form.get("username"):

            rows1 = db.execute("SELECT * FROM users WHERE user_name = ?", request.form.get("username"))

            if len(rows1) != 0:
                flash("Username is not available")
                return redirect(url_for('profile'))
            newRow["user_name"] = request.form.get("username")
        
        if request.form.get("email"):

            rows2 = db.execute("SELECT * FROM users WHERE email = ?", request.form.get("email"))



            if len(rows2) != 0 or not is_email(request.form.get("email"), check_dns=True):
                flash("Email is not available")
                return redirect(url_for('profile'))
            newRow["email"] = request.form.get("email")
        
        if request.form.get("password") or request.form.get("confirmation"):

           
            if request.form.get("password") != request.form.get("confirmation"):
                flash("Must provide a password and confirm it")
                return redirect(url_for('profile'))
            newRow["password"] = generate_password_hash(request.form.get("password"))

        db.execute("UPDATE users set user_name=?, password = ?, email=? where ID=?", newRow["user_name"], newRow[("password")], newRow["email"], newRow["ID"])
        flash("Changes were saved!")
        return render_template("profile.html", row=row)

        

    else:
        
        return render_template("profile.html", row=row)


@app.route("/")
@login_required
def index():
    rows = db.execute("SELECT * FROM routines WHERE user_id = ?", session["user_id"])
   
    return render_template("index.html", rows=rows )



@app.route("/add", methods=["GET", "POST"])
@login_required
def add():
    status = ["Done-On-Time", "Done","Not-Set", "Missed"]

    if request.method == "POST":
        newRoutine = {}
        newRoutine["user_id"] = session["user_id"]
        if not request.form.get("name"):
            flash("Please Enter Task Name")
            return redirect(url_for('add'))
        else:
            newRoutine["name"] = request.form.get("name")
            
            newRoutine["description"] = request.form.get("description") if request.form.get("description") else ""
            
            if not request.form.get("priority"):
               newRoutine["priority"] = 1
            elif request.form.get("priority").isdigit() and int( request.form.get("priority")) > 0  and int( request.form.get("priority")) < 6:
                newRoutine["priority"] = int(request.form.get("priority"))

            else:
                 newRoutine["priority"] = 1
                

            newRoutine["start-date"] = request.form.get("start-date") if request.form.get("start-date") else datetime.now().strftime('%Y-%m-%d')
            newRoutine["status"] = request.form.get("status") if request.form.get("status") in status else "Not-Set"
        db.execute("INSERT INTO routines(user_id, name, description, priority,start_date, status ) VALUES(?,?,?,?,?,?)",newRoutine["user_id"], newRoutine["name"], newRoutine["description"], newRoutine["priority"], newRoutine["start-date"], newRoutine["status"])

        return redirect("/")      
    else:
        return render_template("add.html")



@app.route('/<int:routine_id>/delete', methods=['POST'])
@login_required
def deleteRoutine(routine_id):
    
    if request.method == 'POST':
        rows = db.execute("DELETE FROM routines WHERE ID = ? AND user_id=?", routine_id, session["user_id"])

        return redirect(url_for('index'))
   
   

@app.route("/<int:routine_id>/edit", methods=["GET", "POST"])
@login_required
def edit(routine_id):
    status = ["Done-On-Time", "Done","Not-Set", "Missed"]

    rows = db.execute("SELECT * FROM routines WHERE ID = ?", routine_id)
    row = rows[0]
    if request.method == "POST":
        newRoutine = {}
        if not request.form.get("name"):
            flash("Please Enter Task Name")
            return redirect(url_for('add'))
        else:
            newRoutine["name"] = request.form.get("name")
            
            newRoutine["description"] = request.form.get("description") if request.form.get("description") else ""
            
            if not request.form.get("priority"):
               newRoutine["priority"] = 1

            elif request.form.get("priority").isdigit() and int( request.form.get("priority")) > 0  and int( request.form.get("priority")) < 6:
                newRoutine["priority"] = int(request.form.get("priority"))

            else:
                 newRoutine["priority"] = 1
                

            newRoutine["start-date"] = request.form.get("start-date") if request.form.get("start-date") else datetime.now().strftime('%Y-%m-%d')

            newRoutine["end-date"] = request.form.get("end-date") if request.form.get("end-date") else ""

            newRoutine["status"] = request.form.get("status") if request.form.get("status") in status else "Not-Set"
        
        

        db.execute("UPDATE routines set name=?, description=?, priority=?,start_date=?, end_date=?, status=? where ID= ? AND user_id=?",newRoutine["name"], newRoutine["description"], newRoutine["priority"], newRoutine["start-date"], newRoutine["end-date"], newRoutine["status"], routine_id, session["user_id"])
        flash("Changes were saved!")
        return redirect("/")      
    else:
        return render_template("edit.html",routine_id=routine_id, row= row)



@app.route('/<int:routine_id>/update', methods=['POST'])
@login_required
def update(routine_id):
    
    if request.method == 'POST':
        rows = db.execute("DELETE FROM routines WHERE ID = ?", routine_id)

        return redirect(url_for('index'))