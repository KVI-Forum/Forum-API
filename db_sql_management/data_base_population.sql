-- Insert into categories
INSERT INTO `forumdb`.`categories` (`name`, `description`) VALUES
('General Discussion', 'A place for general conversations'),
('Tech Talk', 'Discuss technology here'),
('Gaming', 'Talk about video games and gaming trends'),
('News', 'Share and discuss the latest news'),
('Feedback', 'Give feedback on the forum');

-- Insert into users (at least one admin)
INSERT INTO `forumdb`.`users` (`first_name`, `last_name`, `username`, `is_admin`, `password`, `email`) VALUES
('John', 'Doe', 'johndoe', 1, 'password123', 'johndoe@example.com'), -- Admin user
('Jane', 'Smith', 'janesmith', 0, 'password123', 'janesmith@example.com'),
('Michael', 'Brown', 'michaelb', 0, 'password123', 'michaelb@example.com'),
('Sara', 'Connor', 'saraconnor', 0, 'password123', 'saraconnor@example.com'),
('David', 'Lee', 'davidlee', 0, 'password123', 'davidlee@example.com');

-- Insert into access
INSERT INTO `forumdb`.`access` (`users_id`, `categories_id`, `access_type`) VALUES
(1, 1, 0), -- Admin full access to General Discussion
(2, 2, 1), -- Jane read-only access to Tech Talk
(3, 3, 0), -- Michael full access to Gaming
(4, 4, 0), -- Sara full access to News
(5, 5, 1); -- David read-only access to Feedback

-- Insert into conversation (private messaging between users)
INSERT INTO `forumdb`.`conversation` (`users_id1`, `users_id2`) VALUES
(1, 2), -- Conversation between John and Jane
(3, 4); -- Conversation between Michael and Sara

-- Insert into messages (within the conversations)
INSERT INTO `forumdb`.`messages` (`text`, `conversation_id`, `users_id`) VALUES
('Hey Jane, how are you?', 1, 1),
('I am good, how about you?', 1, 2),
('Hi Sara, do you want to join the game?', 2, 3),
('Sure, I am ready!', 2, 4);

-- Insert into topics
INSERT INTO `forumdb`.`topics` (`name`, `categories_id`, `author_id`) VALUES
('Welcome to the forum', 1, 1),
('Latest Tech News', 2, 2),
('Top Gaming Trends', 3, 3),
('Breaking News Today', 4, 4),
('Forum Feedback and Suggestions', 5, 5);

-- Insert into reply (replies to topics)
INSERT INTO `forumdb`.`reply` (`content`, `topics_id`, `users_id`) VALUES
('Thanks for the welcome, John!', 1, 2),
('Interesting tech news!', 2, 3),
('Loving the gaming trends!', 3, 4),
('Breaking news indeed!', 4, 5),
('Here is my feedback for the forum.', 5, 1);

-- Insert into votes (votes on replies)
INSERT INTO `forumdb`.`votes` (`users_id`, `reply_id`, `type_vote`) VALUES
(1, 1, 1), -- John upvotes Jane's reply
(2, 2, 1), -- Jane upvotes Michael's reply
(3, 3, 1), -- Michael upvotes Sara's reply
(4, 4, 1), -- Sara upvotes David's reply
(5, 5, 1); -- David upvotes John's reply
