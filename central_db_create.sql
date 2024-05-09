-- Active: 1705509733487@@127.0.0.1@3306
-- Create a sample Central DATABASE and User

DROP DATABASE IF EXISTS `central_db`;
CREATE DATABASE IF NOT EXISTS `central_db`;
CREATE USER IF NOT EXISTS 'my_user'@'localhost' IDENTIFIED BY 'my_user_passwd';
GRANT ALL PRIVILEGES ON central_db.* TO 'my_user'@'localhost';
FLUSH PRIVILEGES;

USE `central_db`;


-- CREATE TABLE user_database (
--     id INT AUTO_INCREMENT PRIMARY KEY,
--     db_list JSON
-- );

INSERT INTO `user_database` (username, db_list) VALUES
("Rashisky", '{"postgresql": [["adejare", "2011-11-11"]], "mysql+mysqldb": [["dummy3", "2024-05-05"], ["tv_shows", "2024-05-05"]]}'),
("Paper", '{"mariadb": [["porche", "2011-01-01"], ["testing", "2020-04-08"]]}'),
("abc", '{"mysql+mysqldb": [["hbnb_dev_db", "2024-05-08"], ["parche", "2023-02-09"]]}'),
("def", '{"mariadb": [["porche", "1999-03-02"], ["testing", "2000-04-04"]]}'),
("ghi", '{"postgresql": [["hbnb_dev_db", "2018-05-17"], ["testing", "2015-07-23"]]}'),
("jkl", '{"mysql+mysqldb": [["dummy3", "2024-05-05"], ["hbnb_dev_db", "2024-05-05"]]}'),
("mno", '{"postgresql": [["adejare", "2024-06-15"]], "mysql+mysqldb": [["hbnb_dev_db", "2024-05-05"], ["tv_shows", "2024-05-07"]]}');
