import sqlite3

connection = sqlite3.connect("decision.db")

connection.execute("DELETE FROM scores")

connection.commit()
connection.close()

print("Scores cleared.")
