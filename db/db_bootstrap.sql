-- This file is to bootstrap a database for the CS3200 project. 
SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0;
SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0;
SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='TRADITIONAL,ALLOW_INVALID_DATES';

DROP SCHEMA IF EXISTS `dockter` ;
CREATE SCHEMA IF NOT EXISTS `dockter` DEFAULT CHARACTER SET latin1 ;
USE `dockter` ;

-- Create a new database.  You can change the name later.  You'll
-- need this name in the FLASK API file(s),  the AppSmith 
-- data source creation.
create database dockter;

-- Via the Docker Compose file, a special user called webapp will 
-- be created in MySQL. We are going to grant that user 
-- all privilages to the new database we just created. 
-- TODO: If you changed the name of the database above, you need 
-- to change it here too.
grant all privileges on dockter.* to 'webapp'@'%';
flush privileges;

-- Move into the database we just created.
-- TODO: If you changed the name of the database above, you need to
-- change it here too. 
use dockter;

-- Put your DDL 
CREATE TABLE IF NOT EXISTS patient (
  patient_id INT PRIMARY KEY,
  first_name VARCHAR(20) NOT NULL,
  middle_name VARCHAR(20),
  last_name VARCHAR(20) NOT NULL,
  phone VARCHAR(20),
  street_address VARCHAR(10)
  state VARCHAR(100),
  city VARCHAR(200),
  zipcode VARCHAR(50),
  policy_id INT,
  insurance_rep_id INT,
  FOREIGN KEY policy_id references insurance_plan (policy_id)
  FOREIGN KEY (insurancerepid) references insurance_rep (insurance_rep_id)
);

CREATE TABLE IF NOT EXISTS insurance_plan (
  policy_id INT PRIMARY KEY,
  plan_name VARCHAR500) NOT NULL,
  company_id INT,
  FOREIGN KEY company_id references insurance_company (company_id)
);

CREATE TABLE IF NOT EXISTS insurance_rep (
  insure_rep_ID INT PRIMARY KEY,
  first_name VARCHAR(20) NOT NULL,
  last_name VARCHAR(20) NOT NULL,
  company_id INT,
  FOREIGN KEY company_id references insurance_company (company_id)
);

CREATE TABLE IF NOT EXISTS insurance_company (
  company_id INT PRIMARY KEY,
  company_name VARCHAR(50)
);

CREATE TABLE IF NOT EXISTS medical_history (
  record_id INT PRIMARY KEY,
  patient_id INT,
  FOREIGN KEY patient_id references patient (patient_id)
);

CREATE TABLE IF NOT EXISTS appointment (
);

CREATE TABLE IF NOT EXISTS availability (
);

CREATE TABLE IF NOT EXISTS medical_professional (
);

CREATE TABLE IF NOT EXISTS services (
);
CREATE TABLE IF NOT EXISTS healthcare_admin_employee (
);
CREATE TABLE IF NOT EXISTS medical_center (
);
CREATE TABLE IF NOT EXISTS conditions (
);
-- Add sample data. 
INSERT INTO test_table
  (name, color)
VALUES
  ('dev', 'blue'),
  ('pro', 'yellow'),
  ('junior', 'red');