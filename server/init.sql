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
    username VARCHAR(200) NOT NULL,
    password VARCHAR(200) NOT NULL,
    type VARCHAR(200) NOT NULL,
    PRIMARY KEY (id),
    INDEX (username)
);

INSERT INTO users (username, password) VALUES ('admin', 'admin');      