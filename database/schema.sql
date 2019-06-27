CREATE TABLE ecosystem (
    id            INTEGER PRIMARY KEY ASC,
    name          TEXT NOT NULL,
    description   TEXT,
    index_url     TEXT
);

CREATE TABLE package (
    id            INTEGER PRIMARY KEY ASC,
    ecosystem     INTEGER NOT NULL,
    description   TEXT,
    package_url   TEXT,
    repo_url      TEXT,
    FOREIGN KEY(ecosystem) REFERENCES ecosystem(id)
);

CREATE TABLE package_index (
    id            INTEGER PRIMARY KEY ASC,
    ecosystem     INTEGER NOT NULL,
    name          TEXT NOT NULL,
    url           TEXT NOT NULL,
    FOREIGN KEY(ecosystem) REFERENCES ecosystem(id)
);

CREATE TABLE popular_packages_index (
    id            INTEGER PRIMARY KEY ASC,
    ecosystem     INTEGER NOT NULL,
    name          TEXT NOT NULL,
    url           TEXT NOT NULL,
    FOREIGN KEY(ecosystem) REFERENCES ecosystem(id)
);

