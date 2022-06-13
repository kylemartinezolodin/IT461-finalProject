CREATE DATABASE electronickxz;

USE electronickxz;

CREATE TABLE items(
    id INT NOT NULL AUTO_INCREMENT,
    name VARCHAR(200) NOT NULL,
    quantity INT NOT NULL,
    price float(5,2) NOT NULL,
    PRIMARY KEY (id),
    INDEX (name)
);

CREATE TABLE users(
    id INT NOT NULL AUTO_INCREMENT,
    fname VARCHAR(200) NOT NULL,
    lname VARCHAR(200) NOT NULL,
    username VARCHAR(200) NOT NULL,
    password VARCHAR(200) NOT NULL,
    type VARCHAR(200) NOT NULL,
    PRIMARY KEY (id),
    INDEX (username)
);

INSERT INTO users (username, password, type, fname, lname) VALUES ('admin', 'admin', 'editor', 'admin', 'admin');
INSERT INTO users (username, password, type, fname, lname) VALUES ('guest', 'guest', 'guest', 'guest', 'guest');