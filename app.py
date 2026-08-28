import sqlite3
from flask import Flask, render_template, request

app = Flask(__name__)


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/create", methods=["GET", "POST"])
def create():
    if request.method == "POST":
        title = request.form.get("title")

        connection = sqlite3.connect("decision.db")

        connection.execute(
            "INSERT INTO decisions (title) VALUES (?)",
            (title,)
        )

        connection.commit()
        connection.close()

        return f"You created: {title}"

    return render_template("create.html")
