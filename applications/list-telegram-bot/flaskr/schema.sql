DROP TABLE IF EXISTS schedule;

CREATE TABLE schedule (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    link TEXT,
    time TEXT,
    category TEXT NOT NULL
);