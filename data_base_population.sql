-- Insert data into categories table
INSERT INTO `forumdb`.`categories` (`name`, `description`)
VALUES
('General Discussion', 'A place for general forum topics.'),
('Tech Support', 'Help and support for technical issues.'),
('Off-Topic', 'Casual conversations and off-topic discussions.');

-- Insert data into users table
INSERT INTO `forumdb`.`users` (`first_name`, `last_name`, `username`, `is_admin`, `password`, `email`)
VALUES
('John', 'Doe', 'johndoe', 1, 'password123', 'john@example.com'),
('Jane', 'Smith', 'janesmith', 0, 'password456', 'jane@example.com'),
('Alice', 'Johnson', 'alicej', 0, 'password789', 'alice@example.com'),
('Bob', 'Brown', 'bobbrown', 0, 'password321', 'bob@example.com');

-- Now you can insert into child tables referencing users and categories

-- Insert data into access table
INSERT INTO `forumdb`.`access` (`users_id`, `categories_id`, `read_only`)
VALUES
(1, 1, 0),
(2, 1, 1),
(3, 2, 0),
(4, 3, 1);

-- Insert data into topics table
INSERT INTO `forumdb`.`topics` (`id`, `name`, `created_at`)
VALUES
(1, 'Welcome to the Forum', '2024-09-30 09:00:00'),
(2, 'Technical Issues', '2024-10-01 10:00:00'),
(3, 'Off-Topic Chat', '2024-10-02 11:30:00');

-- Insert data into conversation table
INSERT INTO `forumdb`.`conversation` (`id`, `users_id1`, `users_id2`, `created_at`)
VALUES
(1, 1, 2, '2024-10-01 12:30:00'),
(2, 2, 3, '2024-10-02 15:45:00');

-- Insert data into massages table
INSERT INTO `forumdb`.`massages` (`id`, `text`, `conversation_id`, `users_id`, `sended_at`)
VALUES
(1, 'Hello, how are you?', 1, 1, '2024-10-01 12:31:00'),
(2, 'I am fine, thank you!', 1, 2, '2024-10-01 12:32:00'),
(3, 'Do you need help?', 2, 2, '2024-10-02 15:50:00'),
(4, 'Yes, I do.', 2, 3, '2024-10-02 15:51:00');

-- Insert data into reply table
INSERT INTO `forumdb`.`reply` (`id`, `content`, `topics_id`, `users_id`, `created_at`)
VALUES
(1, 'Thanks for creating this forum!', 1, 1, '2024-09-30 09:30:00'),
(2, 'I have a problem with my computer.', 2, 2, '2024-10-01 10:15:00'),
(3, 'What do you need help with?', 2, 3, '2024-10-01 10:20:00'),
(4, 'Any good movie recommendations?', 3, 4, '2024-10-02 12:00:00');

-- Insert data into votes table
INSERT INTO `forumdb`.`votes` (`users_id`, `reply_id`, `type_vote`, `created_at`)
VALUES
(1, 1, 1, '2024-09-30 09:35:00'),
(2, 2, -1, '2024-10-01 10:30:00'),
(3, 3, 1, '2024-10-01 10:25:00'),
(4, 4, 1, '2024-10-02 12:05:00');
