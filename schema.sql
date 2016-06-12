DROP TABLE IF EXISTS answers;
DROP TABLE IF EXISTS questions;

CREATE TABLE questions(
  Id SERIAL PRIMARY KEY,
  Body VARCHAR(255)
);

CREATE TABLE answers(
  Id SERIAL PRIMARY KEY,
  Body VARCHAR(255),
  Correct BOOLEAN,
  Question_id INT REFERENCES questions(id)
);
