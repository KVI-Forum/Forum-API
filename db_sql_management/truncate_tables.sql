-- Disable foreign key checks to avoid constraint errors while truncating
SET FOREIGN_KEY_CHECKS=0;

-- Truncate child tables first
TRUNCATE TABLE `votes`;
TRUNCATE TABLE `reply`;
TRUNCATE TABLE `messages`;
TRUNCATE TABLE `conversation`;

-- Truncate parent tables
TRUNCATE TABLE `topics`;
TRUNCATE TABLE `users`;
TRUNCATE TABLE `categories`;

-- Re-enable foreign key checks
SET FOREIGN_KEY_CHECKS=1;