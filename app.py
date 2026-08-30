import sqlite3
from flask import Flask, render_template, request

app = Flask(__name__)


@app.route("/")
def index():
    connection = sqlite3.connect("decision.db")

    decisions = connection.execute(
        "SELECT id, title FROM decisions"
    ).fetchall()

    connection.close()

    return render_template("index.html", decisions=decisions)


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


@app.route("/decision/<int:decision_id>")
def decision_detail(decision_id):
    connection = sqlite3.connect("decision.db")

    decision = connection.execute(
        "SELECT id, title FROM decisions WHERE id = ?",
        (decision_id,)
    ).fetchone()

    connection.close()

    return render_template("decision.html", decision=decision)


if __name__ == "__main__":
    app.run(debug=True)
