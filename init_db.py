import sqlite3

connection = sqlite3.connect("decision.db")

with open("schema.sql") as file:
    connection.executescript(file.read())

connection.close()
