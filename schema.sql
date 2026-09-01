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

CREATE TABLE scores (
    id INTEGER PRIMARY KEY,
    alternative_id INTEGER NOT NULL,
    criterion_id INTEGER NOT NULL,
    value REAL NOT NULL,
    FOREIGN KEY (alternative_id) REFERENCES alternatives(id),
    FOREIGN KEY (criterion_id) REFERENCES criteria(id),
    UNIQUE (alternative_id, criterion_id)
);