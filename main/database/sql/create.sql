CREATE TABLE language(
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL UNIQUE
);

CREATE TABLE search(
    id INTEGER PRIMARY KEY,
    date TEXT NOT NULL,
    language INTEGER NOT NULL,
    min_size INTEGER NOT NULL,
    max_size INTEGER,
    min_number_of_stars INTEGER,
    max_number_of_stars INTEGER,
    number_of_stars INTEGER,
    min_number_of_contributors INTEGER NOT NULL,
    max_number_of_contributors INTEGER,
    FOREIGN KEY(language) REFERENCES language(id)
);

CREATE TABLE repository(
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL,
    url TEXT NOT NULL UNIQUE,
    size INTEGER NOT NULL,
    number_of_stars INTEGER NOT NULL,
    number_of_contributors INTEGER,
    analyzed INTEGER NOT NULL DEFAULT 0
);

CREATE TABLE search_repository(
    search INTEGER NOT NULL,
    repository INTEGER NOT NULL,
    FOREIGN KEY(search) REFERENCES search(id),
    FOREIGN KEY(repository) REFERENCES repository(id)
);

CREATE TABLE result(
    id INTEGER PRIMARY KEY,
    search INTEGER NOT NULL,
    repository INTEGER NOT NULL,
    sqliv INTEGER, -- TODO NOT NULL,
    size INTEGER NOT NULL,
    number_of_stars INTEGER NOT NULL,
    number_of_contributors INTEGER,
    FOREIGN KEY(search) REFERENCES search(id),
    FOREIGN KEY(repository) REFERENCES repository(id)
);

CREATE TABLE sqliv(
    result INTEGER NOT NULL,
    file_relative_repo TEXT NOT NULL,
    location TEXT NOT NULL,
    type TEXT NOT NULL,
    FOREIGN KEY(result) REFERENCES result(id)
);
