CREATE TABLE Text (
    id INTEGER PRIMARY KEY ASC,
    work TEXT NOT NULL,
    siglum TEXT NOT NULL,
    checksum TEXT NOT NULL,
    token_count INTEGER NOT NULL,
    label TEXT NOT NULL,

    UNIQUE (work, siglum)
);

CREATE TABLE TextHasNGram (
    text INTEGER NOT NULL REFERENCES Text (id) ON DELETE CASCADE,
    size INTEGER NOT NULL,
    count INTEGER NOT NULL
);