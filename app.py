from flask import Flask, render_template, session, redirect, url_for, request
from flask_session import Session
from tempfile import mkdtemp
import os
import sys
import csv
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

engine = create_engine(os.getenv("DATABASE_URL"))
db = scoped_session(sessionmaker(bind=engine))

app = Flask(__name__)

app.config["SESSION_FILE_DIR"] = mkdtemp()
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

@app.route("/", methods=["GET", "POST"])
def home():
    if request.method == "GET":
        return render_template("book.html")
    title = request.form.get("title")
    print("reached")
    test = db.execute("SELECT * FROM flights").fetchone()
    print(test)
    print(title)
    book = db.execute("SELECT title, author_id, year, isbn FROM books WHERE title=:title", {"title":title}).fetchone()
    if book is None:
        return render_template("book.html", sorry=True, title = title)
    author = db.execute("SELECT name FROM authors WHERE id=:id", {"id":book[1]}).fetchone()[0]

    return render_template("result.html", title=book[0], author=author, year=book[2], isbn=book[3])
