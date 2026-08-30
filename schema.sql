CREATE TABLE decisions (
    id INTEGER PRIMARY KEY,
    title TEXT NOT NULL
);

CREATE TABLE alternatives (
    id INTEGER PRIMARY KEY,
    decision_id INTEGER NOT NULL,
    name TEXT NOT NULL,
    FOREIGN KEY (decision_id) REFERENCES decisions(id)
);

CREATE TABLE criteria (
    id INTEGER PRIMARY KEY,
    decision_id INTEGER NOT NULL,
    name TEXT NOT NULL,
    weight REAL NOT NULL,
    FOREIGN KEY (decision_id) REFERENCES decisions(id)
);