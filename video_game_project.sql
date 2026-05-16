-- MySQL Workbench Forward Engineering

SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0;
SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0;
SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION';

-- -----------------------------------------------------
-- Schema video_game_db
-- -----------------------------------------------------

-- -----------------------------------------------------
-- Schema video_game_db
-- -----------------------------------------------------
CREATE SCHEMA IF NOT EXISTS `video_game_db` DEFAULT CHARACTER SET utf8 ;
USE `video_game_db` ;

-- -----------------------------------------------------
-- Table `video_game_db`.`games`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `video_game_db`.`games` (
  `game_id` INT NOT NULL AUTO_INCREMENT,
  `title` VARCHAR(100) NOT NULL,
  `release_year` INT NULL,
  `developer` VARCHAR(100) NULL,
  PRIMARY KEY (`game_id`))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `video_game_db`.`platforms`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `video_game_db`.`platforms` (
  `platform_id` INT NOT NULL AUTO_INCREMENT,
  `platform_name` VARCHAR(45) NOT NULL,
  PRIMARY KEY (`platform_id`))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `video_game_db`.`genres`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `video_game_db`.`genres` (
  `genre_id` INT NOT NULL AUTO_INCREMENT,
  `genre_name` VARCHAR(45) NOT NULL,
  PRIMARY KEY (`genre_id`))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `video_game_db`.`game_platforms`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `video_game_db`.`game_platforms` (
  `game_id` INT NOT NULL,
  `platform_id` INT NOT NULL,
  PRIMARY KEY (`game_id`, `platform_id`),
  INDEX `fk_game_platforms_platform_idx` (`platform_id` ASC),
  CONSTRAINT `fk_game_platforms_game`
    FOREIGN KEY (`game_id`)
    REFERENCES `video_game_db`.`games` (`game_id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_game_platforms_platform`
    FOREIGN KEY (`platform_id`)
    REFERENCES `video_game_db`.`platforms` (`platform_id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `video_game_db`.`game_genres`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `video_game_db`.`game_genres` (
  `game_id` INT NOT NULL,
  `genre_id` INT NOT NULL,
  PRIMARY KEY (`game_id`, `genre_id`),
  INDEX `fk_game_genres_genre_idx` (`genre_id` ASC),
  CONSTRAINT `fk_game_genres_game`
    FOREIGN KEY (`game_id`)
    REFERENCES `video_game_db`.`games` (`game_id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_game_genres_genre`
    FOREIGN KEY (`genre_id`)
    REFERENCES `video_game_db`.`genres` (`genre_id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


SET SQL_MODE=@OLD_SQL_MODE;
SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS;
SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS;
