-- Setup the db

create database if not exists `finsure`;
create user 'lending_app_user'@'localhost' identified by 'password';
grant all privileges on `finsure`.* to 'lending_app_user'@'localhost';

FLUSH PRIVILEGES;
