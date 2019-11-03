

drop table if exists users;
drop table if exists wearers;
drop table if exists datapoints;
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
    ald BOOLEAN,
    user_id INT NOT NULL,
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

INSERT INTO wearers(name, dob, ald, user_id, created, modified) 
	VALUES ('Wearer_1', '1996-01-01', 1, 3, NOW(), NOW()),
	       ('Wearer_2', '2015-05-23', 1, 3, NOW(), NOW()),
	       ('Wearer_3', '2015-09-14', 0, 3, NOW(), NOW()),
	       ('Wearer_4', '2015-09-14', 0, 4, NOW(), NOW())
	;

#VALUES ('Wearer_3', '2015-01-01', 'TRUE', 2, NOW(), NOW())


INSERT INTO categories(title, description, created, modified)
	VALUES ('SEIZURE', 'An actual seizure event', NOW(), NOW()),
		('NORMAL', 'Generic Normal behaviour event', NOW(), NOW());


INSERT INTO users (uname, password, usertype_id, email, created, modified)
	VALUES
	('admin', '$2y$10$WN2jByiqJZE25uGM8Kl17.OTfKPZBVNB/sx69p7si5oDSz01xv3Vi', 1, 'admin@openseizuredetector.org.uk', NOW(), NOW()),
	('analyst', '$2y$10$OpYQIl8y0fKtDgNSBw7Q..1aPLWuSwWOINc7HFyC.45Alvt24B6IC', 2, 'analyst@openseizuredetector.org.uk', NOW(), NOW()),
	('user', '$2y$10$i7W.7sFkSquAoUa40Wf/UuCcn9Jq/X4kBls2gXplEXAEqlRgpQJ8W', 3, 'user@openseizuredetector.org.uk', NOW(), NOW());

INSERT INTO datapoints (dataTime, user_id, wearer_id, accMean, accSd, hr, category_id, dataJSON, created, modified)
	VALUES
	(NOW(), 3, 1, 1000, 100, 70, 1, 'JSONStr1', NOW(), NOW()),
	(NOW(), 3, 1, 1100, 90, 71, 1, 'JSONStr2', NOW(), NOW()),
	(NOW(), 3, 1, 1050, 110, 72, 1, 'JSONStr3', NOW(), NOW()),
	(NOW(), 2, 3, 1200, 80, 73, 1, 'JSONStr4', NOW(), NOW()),
	(NOW(), 4, 2, 1100, 100, 77, 0, 'JSONStr5', NOW(), NOW())
	;
