-- MySQL Workbench Forward Engineering

SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0;
SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0;
SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION';

-- -----------------------------------------------------
-- Schema mydb
-- -----------------------------------------------------
-- -----------------------------------------------------
-- Schema forumdb
-- -----------------------------------------------------

-- -----------------------------------------------------
-- Schema forumdb
-- -----------------------------------------------------
CREATE SCHEMA IF NOT EXISTS `forumdb` ;
USE `forumdb` ;

-- -----------------------------------------------------
-- Table `forumdb`.`categories`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `forumdb`.`categories` (
  `id` INT(11) NOT NULL AUTO_INCREMENT,
  `name` VARCHAR(45) NOT NULL,
  `description` MEDIUMTEXT NULL DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE INDEX `name_UNIQUE` (`name` ASC) VISIBLE)
ENGINE = InnoDB
AUTO_INCREMENT = 6;


-- -----------------------------------------------------
-- Table `forumdb`.`users`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `forumdb`.`users` (
  `id` INT(11) NOT NULL AUTO_INCREMENT,
  `first_name` VARCHAR(45) NOT NULL,
  `last_name` VARCHAR(45) NOT NULL,
  `username` VARCHAR(45) NOT NULL,
  `is_admin` TINYINT(4) NULL DEFAULT NULL,
  `password` VARCHAR(1000) NOT NULL,
  `email` VARCHAR(45) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE INDEX `username_UNIQUE` (`username` ASC) VISIBLE,
  UNIQUE INDEX `email_UNIQUE` (`email` ASC) VISIBLE)
ENGINE = InnoDB
AUTO_INCREMENT = 5;


-- -----------------------------------------------------
-- Table `forumdb`.`access`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `forumdb`.`access` (
  `users_id` INT(11) NOT NULL,
  `categories_id` INT(11) NOT NULL,
  `read_only` TINYINT(4) NULL DEFAULT NULL,
  PRIMARY KEY (`users_id`, `categories_id`),
  INDEX `fk_acsses_users1_idx` (`users_id` ASC) VISIBLE,
  INDEX `fk_acsses_categories1_idx` (`categories_id` ASC) VISIBLE,
  CONSTRAINT `fk_acsses_categories1`
    FOREIGN KEY (`categories_id`)
    REFERENCES `forumdb`.`categories` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_acsses_users1`
    FOREIGN KEY (`users_id`)
    REFERENCES `forumdb`.`users` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `forumdb`.`conversation`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `forumdb`.`conversation` (
  `id` INT(11) NOT NULL,
  `users_id1` INT(11) NOT NULL,
  `users_id2` INT(11) NOT NULL,
  `created_at` DATETIME NULL DEFAULT NULL,
  PRIMARY KEY (`id`),
  INDEX `fk_conversation_users1_idx` (`users_id1` ASC) VISIBLE,
  INDEX `fk_conversation_users2_idx` (`users_id2` ASC) VISIBLE,
  CONSTRAINT `fk_conversation_users1`
    FOREIGN KEY (`users_id1`)
    REFERENCES `forumdb`.`users` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_conversation_users2`
    FOREIGN KEY (`users_id2`)
    REFERENCES `forumdb`.`users` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `forumdb`.`massages`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `forumdb`.`massages` (
  `id` INT(11) NOT NULL,
  `text` VARCHAR(45) NULL DEFAULT NULL,
  `conversation_id` INT(11) NOT NULL,
  `users_id` INT(11) NOT NULL,
  `sended_at` DATETIME NULL DEFAULT NULL,
  PRIMARY KEY (`id`),
  INDEX `fk_massages_conversation1_idx` (`conversation_id` ASC) VISIBLE,
  INDEX `fk_massages_users1_idx` (`users_id` ASC) VISIBLE,
  CONSTRAINT `fk_massages_conversation1`
    FOREIGN KEY (`conversation_id`)
    REFERENCES `forumdb`.`conversation` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_massages_users1`
    FOREIGN KEY (`users_id`)
    REFERENCES `forumdb`.`users` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `forumdb`.`topics`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `forumdb`.`topics` (
  `id` INT(11) NOT NULL,
  `name` VARCHAR(45) NULL DEFAULT NULL,
  `created_at` DATETIME NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE INDEX `idtopics_UNIQUE` (`id` ASC) VISIBLE)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `forumdb`.`reply`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `forumdb`.`reply` (
  `id` INT(11) NOT NULL,
  `content` VARCHAR(300) NULL DEFAULT NULL,
  `topics_id` INT(11) NOT NULL,
  `users_id` INT(11) NOT NULL,
  `created_at` DATETIME NULL DEFAULT NULL,
  PRIMARY KEY (`id`),
  INDEX `fk_reply_topics1_idx` (`topics_id` ASC) VISIBLE,
  INDEX `fk_reply_users1_idx` (`users_id` ASC) VISIBLE,
  CONSTRAINT `fk_reply_topics1`
    FOREIGN KEY (`topics_id`)
    REFERENCES `forumdb`.`topics` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_reply_users1`
    FOREIGN KEY (`users_id`)
    REFERENCES `forumdb`.`users` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `forumdb`.`votes`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `forumdb`.`votes` (
  `users_id` INT(11) NOT NULL,
  `reply_id` INT(11) NOT NULL,
  `type_vote` TINYINT(4) NULL DEFAULT NULL,
  `created_at` DATETIME NULL DEFAULT NULL,
  PRIMARY KEY (`users_id`, `reply_id`),
  INDEX `fk_votes_users1_idx` (`users_id` ASC) VISIBLE,
  INDEX `fk_votes_reply1_idx` (`reply_id` ASC) VISIBLE,
  CONSTRAINT `fk_votes_reply1`
    FOREIGN KEY (`reply_id`)
    REFERENCES `forumdb`.`reply` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_votes_users1`
    FOREIGN KEY (`users_id`)
    REFERENCES `forumdb`.`users` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


SET SQL_MODE=@OLD_SQL_MODE;
SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS;
SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS;