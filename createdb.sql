USE osd;

drop table if exists users;
drop table if exists wearers;
drop table if exists dataPoints;
drop table if exists datapoints;
drop table if exists userTypes;
drop table if exists usertypes;
drop table if exists categories;

CREATE TABLE users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    uname VARCHAR(30) NOT NULL,
    email VARCHAR(255),
    password VARCHAR(255) NOT NULL,
    usertype_id INT NOT NULL,
    created DATETIME,
    modified DATETIME
);

CREATE TABLE wearers (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    dob DATE,
    created DATETIME,
    modified DATETIME
);

CREATE TABLE datapoints (
    id INT AUTO_INCREMENT PRIMARY KEY,
    dataTime DATETIME,
    user_id INT NOT NULL,
    wearer_id INT NOT NULL,
    accMean FLOAT,
    accSd FLOAT,
    hr FLOAT,
    category_id INT,
    dataJSON TEXT,
    created DATETIME,
    modified DATETIME
);


CREATE TABLE usertypes (
   id INT AUTO_INCREMENT PRIMARY KEY,
   title VARCHAR(30),
   description VARCHAR(512),
    created DATETIME,
    modified DATETIME
);

CREATE TABLE categories (
   id INT AUTO_INCREMENT PRIMARY KEY,
   title VARCHAR(30),
   description VARCHAR(512),
    created DATETIME,
    modified DATETIME
);

INSERT INTO usertypes(title, description, created, modified) 
	VALUES ('ADMIN', 'Administrator - full access to data', NOW(), NOW()),
	       ('ANALYST', 'Data Analyst - access to all anomysed data', NOW(), NOW()),
               ('USER', 'Normal user - can upload and modify their own data only', NOW(), NOW())
	;

INSERT INTO categories(title, description, created, modified)
	VALUES ('SEIZURE', 'An actual seizure event', NOW(), NOW()),
		('NORMAL', 'Generic Normal behaviour event', NOW(), NOW());


INSERT INTO users (uname, password, usertype_id, email, created, modified)
	VALUES
	('admin', 'admin_pw', 0, 'admin@openseizuredetector.org.uk', NOW(), NOW()),
	('analyst_test1', 'analyst_test1_pw', 1, 'admin@openseizuredetector.org.uk', NOW(), NOW()),
	('user_test1', 'user_test1_pw', 2, 'admin@openseizuredetector.org.uk', NOW(), NOW());

INSERT INTO datapoints (dataTime, user_id, wearer_id, accMean, accSd, hr, category_id, dataJSON, created, modified)
	VALUES
	(NOW(), 0, 0, 1000, 100, 70, 1, 'JSONStr', NOW(), NOW()),
	(NOW(), 0, 0, 1100, 90, 71, 1, 'JSONStr', NOW(), NOW()),
	(NOW(), 0, 0, 1050, 110, 72, 1, 'JSONStr', NOW(), NOW()),
	(NOW(), 0, 0, 1200, 80, 73, 1, 'JSONStr', NOW(), NOW()),
	(NOW(), 0, 0, 1100, 100, 77, 0, 'JSONStr', NOW(), NOW())
	;
