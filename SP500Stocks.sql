SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0;
SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0;
SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='TRADITIONAL,ALLOW_INVALID_DATES';

CREATE SCHEMA IF NOT EXISTS `SP500` DEFAULT CHARACTER SET utf8 COLLATE utf8_general_ci ;
USE `SP500` ;

-- -----------------------------------------------------
-- Table `SP500`.`Stocks`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `SP500`.`Stocks` ;

CREATE TABLE IF NOT EXISTS `SP500`.`Stocks` (
  `pkStocks` INT NOT NULL,
  `date` DATE NOT NULL,
  `opening` DECIMAL(13,6) NOT NULL,
  `high` DECIMAL(13,6) NOT NULL,
  `low` DECIMAL(13,6) NOT NULL,
  `closing` DECIMAL(13,6) NOT NULL,
  `adjustClosing` DECIMAL(13,6) NOT NULL,
  `volume` DECIMAL(13,1) NOT NULL,
  `companyAbbreviation` VARCHAR(8) NOT NULL,
  `companyName` VARCHAR(50) NOT NULL,
  `sector` VARCHAR(30) NOT NULL,
  PRIMARY KEY (`pkStocks`),
  UNIQUE INDEX `pkStocks_UNIQUE` (`pkStocks` ASC))
ENGINE = InnoDB;


SET SQL_MODE=@OLD_SQL_MODE;
SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS;
SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS;

LOAD DATA INFILE '/var/lib/mysql-files/Stocks.csv'
INTO TABLE `Stocks` 
FIELDS TERMINATED BY ','
LINES TERMINATED BY '\n'
IGNORE 1 LINES;
(@pkStocks, date, opening, high, low, closing, adjustClosing, volume, companyAbbreviation, companyName, sector)
SET pkStocks = @pkStocks + 1 # Start at 1 instead of 0 for the primary key.


CREATE OR REPLACE VIEW GroupedStocksByCiesAndYears AS
	SELECT companyName, 
		   YEAR(date) AS year_date,
		   SUBSTRING_INDEX(GROUP_CONCAT(CAST(opening AS CHAR) ORDER BY date), ',', 1) AS first_open,
		   SUBSTRING_INDEX(GROUP_CONCAT(CAST(closing AS CHAR) ORDER BY date DESC), ',', 1) AS last_close
	FROM Stocks
	GROUP BY companyName, year_date
	ORDER BY companyName ASC
