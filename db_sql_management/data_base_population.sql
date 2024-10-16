-- Insert data into the `categories` table
INSERT INTO `forumdb`.`categories` (`name`, `description`) VALUES
('General Discussion', 'A place for general discussions'),
('Announcements', 'Important announcements and updates'),
('Feedback', 'Share your feedback and suggestions');

-- Insert data into the `users` table
INSERT INTO `forumdb`.`users` (`first_name`, `last_name`, `username`, `is_admin`, `password`, `email`) VALUES
('John', 'Doe', 'johndoe', 1, 'password123', 'johndoe@example.com'),
('Jane', 'Smith', 'janesmith', 0, 'password123', 'janesmith@example.com'),
('Bob', 'Johnson', 'bobjohnson', 0, 'password123', 'bobjohnson@example.com');

-- Insert data into the `access` table
INSERT INTO `forumdb`.`access` (`users_id`, `categories_id`, `read_only`) VALUES
(1, 1, 0),  -- Admin has full access to General Discussion
(2, 1, 1),  -- Jane has read-only access to General Discussion
(3, 3, 0);  -- Bob has full access to Feedback

-- Insert data into the `conversation` table
INSERT INTO `forumdb`.`conversation` (`users_id1`, `users_id2`, `created_at`) VALUES
(1, 2, NOW()),  -- Conversation between John and Jane
(1, 3, NOW());  -- Conversation between John and Bob

-- Insert data into the `messages` table
INSERT INTO `forumdb`.`messages` (`text`, `conversation_id`, `users_id`, `sent_at`) VALUES
('Hey Jane, how are you?', 1, 1, NOW()),
('I\'m doing well, thanks!', 1, 2, NOW()),
('Hey Bob, any feedback on the new update?', 2, 1, NOW());

-- Insert data into the `topics` table
INSERT INTO `forumdb`.`topics` (`name`, `created_at`, `categories_id`) VALUES
('Welcome to the Forum', NOW(), 1),
('New Forum Update', NOW(), 2);

-- Insert data into the `reply` table
INSERT INTO `forumdb`.`reply` (`content`, `topics_id`, `users_id`, `created_at`) VALUES
('This looks great, thanks for the update!', 2, 2, NOW()),
('I love the new features!', 2, 3, NOW());

-- Insert data into the `votes` table
INSERT INTO `forumdb`.`votes` (`users_id`, `reply_id`, `type_vote`, `created_at`) VALUES
(1, 1, 1, NOW()),  -- John upvotes Jane's reply
(2, 2, 1, NOW());  -- Jane upvotes Bob's reply
