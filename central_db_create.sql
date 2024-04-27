-- Create a sample Central DATABASE and User

DROP DATABASE IF EXISTS `central_db`;
CREATE DATABASE IF NOT EXISTS `central_db`;
CREATE USER IF NOT EXISTS 'my_user'@'localhost' IDENTIFIED BY 'my_user_passwd';
GRANT ALL PRIVILEGES ON central_db.* TO 'my_user'@'localhost';
FLUSH PRIVILEGES;
