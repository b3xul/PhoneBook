CREATE DATABASE IF NOT EXISTS phone_book;
USE phone_book;

CREATE TABLE contatti (
  id INT AUTO_INCREMENT PRIMARY KEY,
  nome VARCHAR(255) NOT NULL,
  cognome VARCHAR(255) NOT NULL,
  indirizzo VARCHAR(255),
  telefono VARCHAR(255) NOT NULL,
  eta TINYINT UNSIGNED
);

INSERT INTO contatti (nome, cognome, indirizzo, telefono, eta)
VALUES  ('Steve', 'Jobs', 'via Cupertino 13', '0612344', 56),
        ('Bill', 'Gates', 'via Redmond 10', '06688989', 60),
        ('Babbo', 'Natale', 'via del Polo Nord', '00000111', 99);