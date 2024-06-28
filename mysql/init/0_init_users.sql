CREATE DATABASE IF NOT EXISTS `faz-bot`;
CREATE DATABASE IF NOT EXISTS `faz-bot_test`;
CREATE DATABASE IF NOT EXISTS `faz-db`;
CREATE DATABASE IF NOT EXISTS `faz-db_test`;

CREATE USER IF NOT EXISTS 'fazbot'@'%' IDENTIFIED BY 'password';
GRANT ALL PRIVILEGES ON `faz-bot`.* TO 'fazbot'@'%';
GRANT ALL PRIVILEGES ON `faz-bot_test`.* TO 'fazbot'@'%';
GRANT ALL PRIVILEGES ON `faz-db`.* TO 'fazbot'@'%';
GRANT ALL PRIVILEGES ON `faz-db_test`.* TO 'fazbot'@'%';
FLUSH PRIVILEGES;
