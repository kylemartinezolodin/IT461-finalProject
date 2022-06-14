CREATE DATABASE electronickxz;

USE electronickxz;

CREATE TABLE items(
    id INT NOT NULL AUTO_INCREMENT,
    name VARCHAR(200) NOT NULL,
    quantity INT NOT NULL,
    price float(10,2) NOT NULL,
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


CREATE TABLE users_cart(
    id INT NOT NULL AUTO_INCREMENT,
    user_id INT NOT NULL,
    item_id INT NOT NULL,
    PRIMARY KEY (id),
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    FOREIGN KEY (item_id) REFERENCES items(id) ON DELETE CASCADE
);

INSERT INTO users (username, password, type, fname, lname) VALUES ('admin', 'admin', 'editor', 'admin', 'admin');
INSERT INTO users (username, password, type, fname, lname) VALUES ('guest', MD5('guest'), 'guest', 'guest', 'guest');