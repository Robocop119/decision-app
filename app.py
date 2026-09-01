import sqlite3
from flask import Flask, render_template, request, redirect
from engine.decision_engine import calculate_score

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
    selected_alternative = request.args.get("alternative", type=int)
    selected_criterion = request.args.get("criterion", type=int)

    connection = sqlite3.connect("decision.db")

    decision = connection.execute(
        "SELECT id, title FROM decisions WHERE id = ?",
        (decision_id,)
    ).fetchone()

    alternatives = connection.execute(
        "SELECT id, name FROM alternatives WHERE decision_id = ?",
        (decision_id,)
    ).fetchall()

    criteria = connection.execute(
        "SELECT id, name, weight FROM criteria WHERE decision_id = ?",
        (decision_id,)
    ).fetchall()

    total_weight = sum(criterion[2] for criterion in criteria)
    weights_valid = abs(total_weight - 1.0) < 0.001

    scores = connection.execute(
        """
        SELECT alternative_id, criterion_id, value
        FROM scores
        """
    ).fetchall()

    ranking = []

    if weights_valid:
        for alternative in alternatives:
            alternative_id = alternative[0]
            alternative_name = alternative[1]

            alternative_scores = [
                score for score in scores
                if score[0] == alternative_id
            ]

            total = calculate_score(criteria, alternative_scores)

            ranking.append((alternative_name, round(total, 2)))

        ranking.sort(key=lambda item: item[1], reverse=True)

    connection.close()

    return render_template(
        "decision.html",
        decision=decision,
        alternatives=alternatives,
        criteria=criteria,
        scores=scores,
        ranking=ranking,
        weights_valid=weights_valid,
        total_weight=total_weight,
        selected_alternative=selected_alternative,
        selected_criterion=selected_criterion
    )


@app.route("/decision/<int:decision_id>/alternative", methods=["POST"])
def add_alternative(decision_id):
    name = request.form.get("name")

    connection = sqlite3.connect("decision.db")

    connection.execute(
        "INSERT INTO alternatives (decision_id, name) VALUES (?, ?)",
        (decision_id, name)
    )

    connection.commit()
    connection.close()

    return redirect(f"/decision/{decision_id}")


@app.route("/decision/<int:decision_id>/criterion", methods=["POST"])
def add_criterion(decision_id):
    name = request.form.get("name")
    weight = request.form.get("weight")

    connection = sqlite3.connect("decision.db")

    connection.execute(
        "INSERT INTO criteria (decision_id, name, weight) VALUES (?, ?, ?)",
        (decision_id, name, weight)
    )

    connection.commit()
    connection.close()

    return redirect(f"/decision/{decision_id}")


@app.route("/decision/<int:decision_id>/score", methods=["POST"])
def add_score(decision_id):
    alternative_id = request.form.get("alternative_id")
    criterion_id = request.form.get("criterion_id")
    value = request.form.get("value")

    connection = sqlite3.connect("decision.db")

    existing_score = connection.execute(
        """
        SELECT id FROM scores
        WHERE alternative_id = ? AND criterion_id = ?
        """,
        (alternative_id, criterion_id)
    ).fetchone()

    if existing_score:
        connection.execute(
            "UPDATE scores SET value = ? WHERE id = ?",
            (value, existing_score[0])
        )
    else:
        connection.execute(
            """
            INSERT INTO scores (alternative_id, criterion_id, value)
            VALUES (?, ?, ?)
            """,
            (alternative_id, criterion_id, value)
        )

    connection.commit()
    connection.close()

    return redirect(
        f"/decision/{decision_id}?alternative={alternative_id}&criterion={criterion_id}"
    )


if __name__ == "__main__":
    app.run(debug=True)
