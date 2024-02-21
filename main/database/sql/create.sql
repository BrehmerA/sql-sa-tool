CREATE TABLE language(
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL UNIQUE
);

CREATE TABLE search(
    id INTEGER PRIMARY KEY,
    date TEXT NOT NULL,
    language INTEGER NOT NULL,
    min_number_of_followers INTEGER NOT NULL,
    min_size INTEGER NOT NULL,
    min_number_of_stars INTEGER NOT NULL,
    FOREIGN KEY(language) REFERENCES language(id)
);

CREATE TABLE repository(
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL,
    url TEXT NOT NULL UNIQUE,
    number_of_followers INTEGER NOT NULL,
    size INTEGER NOT NULL,
    number_of_stars INTEGER NOT NULL
);

CREATE TABLE search_repository(
    search INTEGER NOT NULL,
    repository INTEGER NOT NULL,
    FOREIGN KEY(search) REFERENCES search(id),
    FOREIGN KEY(repository) REFERENCES repository(id)
);
