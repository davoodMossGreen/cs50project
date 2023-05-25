import os

from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.security import check_password_hash, generate_password_hash
from datetime import datetime

from helpers import apology, login_required

# Configure application
app = Flask(__name__)

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True


# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///project.db")


@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


@app.route("/mybooks")
@login_required
def index():
    """Show added books"""
    books = db.execute(
        "SELECT author, title, year, description FROM books WHERE uploader = ? GROUP BY timestamp ORDER BY timestamp DESC", session["user_id"])


    return render_template("mybooks.html", books=books)

@app.route("/add", methods=["GET", "POST"])
@login_required
def add():
    """Add some books"""
    if request.method == "POST":
        author = request.form.get("author")
        title = request.form.get("title")
        description = request.form.get("description")
        year = request.form.get("year")

        if not author or not title or not description or not year:
            return apology("Must fill all the forms to add a book", 400)

        upl_name = db.execute("SELECT username FROM users WHERE id = ?", session["user_id"])

        db.execute("INSERT INTO books (title, author, year, description, uploader, timestamp, uploader_name) VALUES (?, ?, ?, ?, ?, ?, ?)",
        title, author, year, description, session["user_id"], datetime.now(), upl_name[0]["username"])

        flash("Successfully added")
        return render_template("book.html", author=author, title=title, description=description, year=year)

    else:
        return render_template("add.html")

@app.route("/deleteBook", methods=["GET", "POST"])
@login_required
def deleteBook():
    """Delete a book"""
    if request.method == "POST":
        title = request.form.get("title")
        if not title:
            return apology("To delete a book you need to choose its title", 400)
        db.execute("DELETE FROM books WHERE uploader = ? AND title = ?", session["user_id"], title)
        flash("You have successfully deleted a book")
        return redirect("/deleteBook")

    else:
        ttls = db.execute("SELECT title FROM books WHERE uploader = ?", session["user_id"])
        titles = []
        for t in ttls:
            title = t["title"]
            titles.append(title)

        return render_template("deletebooks.html", titles=titles)


@app.route("/history")
@login_required
def history():
    """Show history"""
    rows = db.execute(
        "SELECT author, title, year, timestamp FROM books WHERE uploader = ? GROUP BY timestamp ORDER BY timestamp DESC", session["user_id"])


    return render_template("history.html", events=rows)


@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""

    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Ensure username was submitted
        if not request.form.get("username"):
            return apology("must provide username", 403)

        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password", 403)

        # Query database for username
        rows = db.execute("SELECT * FROM users WHERE username = ?", request.form.get("username"))

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(rows[0]["hash"], request.form.get("password")):
            return apology("invalid username and/or password", 403)

        # Remember which user has logged in
        session["user_id"] = rows[0]["id"]

        # Redirect user to home page
        return redirect("/mybooks")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("login.html")


@app.route("/logout")
def logout():
    """Log user out"""

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/")


@app.route("/book", methods=["GET", "POST"])
@login_required
def quote():
    """Get book info"""
    return apology("TODO")


@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""

    if request.method == "GET":
        return render_template("register.html")
    elif request.method == "POST":
        # Ensure username was submitted
        if not request.form.get("username"):
            return apology("must provide username", 400)
        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password", 400)
        elif not request.form.get("confirmation"):
            return apology("must provide confirmation", 400)
        # Ensure passwords match
        elif request.form.get("password") != request.form.get("confirmation"):
            return apology("passwords don't match", 400)

        # Query database for username
        rows = db.execute("SELECT * FROM users WHERE username = ?", request.form.get("username"))
        if len(rows) > 0:
            return apology("username already exists", 400)

        hashed_pass = generate_password_hash((request.form.get("password")), method='pbkdf2:sha256',
                                            salt_length=len(request.form.get("password")))
        user = db.execute("INSERT INTO users (username, hash) VALUES (?, ?)", request.form.get("username"), hashed_pass)

        session.clear()
        session["user_id"] = user
        return redirect("/mybooks")

@app.route("/")
def allbooks():
    """Show editors' choice"""
    return render_template("index.html")




@app.route("/notes", methods=["GET", "POST"])
@login_required
def notes():
    """Show notes"""
    if request.method == "GET":
        notes = db.execute(
        "SELECT heading, note, date FROM notes WHERE user_id = ? GROUP BY date ORDER BY date DESC", session["user_id"])
        return render_template("notes.html", notes=notes)

    else:
        heading = request.form.get("heading")
        note = request.form.get("note")
        date = datetime.now()

        if not heading or not note:
            return apology("every note must contain a heading and text", 400)

        db.execute(
            "INSERT INTO notes (heading, note, date, user_id) VALUES (?, ?, ?, ?)", heading, note, date, session["user_id"]
            )
        flash("Successfully added")
        return redirect("/notes")


@app.route("/deleteNote", methods=["POST"])
@login_required
def deleteNote():
    """Delete a book"""
    if request.method == "POST":
        heading = request.form.get("heading")
        if not heading:
            return apology("Something went wrong", 400)
        db.execute("DELETE FROM notes WHERE user_id = ? AND heading = ?", session["user_id"], heading)
        flash("You have successfully deleted a note")
        return redirect("/notes")

@app.route("/deleteAccount", methods=["GET", "POST"])
@login_required
def deleteAccount():
    if request.method == "POST":
        yes = request.form.get("Yes")
        nope = request.form.get("No")
        if nope:
            return redirect("/mybooks")
        if yes:
            db.execute("DELETE FROM users WHERE id = ?", session["user_id"])

            session.clear()
            return redirect("/")
    else:
        return render_template("deleteAccount.html")
