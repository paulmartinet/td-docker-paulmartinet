CREATE TABLE IF NOT EXISTS items (
    id SERIAL PRIMARY KEY,
    name TEXT NOT NULL
);

INSERT INTO items (name) VALUES
('Message 1'),
('Message 2'),
('Message 3'),
('Tache 1'),
('Tache 2'),
('Tache 3'),
('Titre 1'),
('Titre 2'),
('Titre 3');