CREATE TABLE IF NOT EXISTS databases (
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL,
    path TEXT NOT NULL,
    corpus_path TEXT NOT NULL,
    ngram_min_length INTEGER NOT NULL,
    ngram_max_length INTEGER NOT NULL
);

CREATE TABLE IF NOT EXISTS results (
    id INTEGER PRIMARY KEY,
    database_id INTEGER NOT NULL,
    path TEXT NOT NULL,
    type TEXT NOT NULL,
    created TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,

    FOREIGN KEY (database_id) REFERENCES databases(id)
        ON UPDATE CASCADE ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS settings (
    last_selected_database_id INTEGER,
    last_open_path TEXT NOT NULL DEFAULT '',
    last_save_path TEXT NOT NULL DEFAULT ''
);