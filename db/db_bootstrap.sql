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
  street_address VARCHAR(100),
  state VARCHAR(50),
  city VARCHAR(50),
  zipcode INT,
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
  insure_rep_id INT PRIMARY KEY,
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
  appoint_id INT PRIMARY KEY,
  time TIME,
  year INT,
  month INT, 
  day INT,
  reason_for_visit VARCHAR(200)
  doc_id INT,
  patient_id INT,
  FOREIGN KEY doc_id references medical_professional (doc_id),
  FOREIGN KEY patient_id references patient (patient_id)
);

CREATE TABLE IF NOT EXISTS availability (
  doc_id INT,
  sched_id INT PRIMARY KEY,
  day_of_week INT,
  start_time TIME, 
  end_time TIME,
  FOREIGN KEY doc_id references medical_professional (doc_id)
);

CREATE TABLE IF NOT EXISTS medical_professional (
  doc_id INT PRIMARY KEY,
  first_name VARCHAR(20),
  last_name VARCHAR(20),
  specialty_name VARCHAR(100),
  admin_id INT,
  FOREIGN KEY admin_id references healthcare_admin_employee (admin_id)
);

CREATE TABLE IF NOT EXISTS services (
  service_id INT PRIMARY KEY,
  service_name VARCHAR(50)
);
CREATE TABLE IF NOT EXISTS healthcare_admin_employee (
  admin_id INT PRIMARY KEY,
  first_name VARCHAR(20),
  last_name VARCHAR(20),
  position VARCHAR(50),
  center_id INT,
  FOREIGN KEY center_id references medical_center (center_id)
);
CREATE TABLE IF NOT EXISTS medical_center (
  center_id INT PRIMARY KEY,
  center_name VARCHAR(50),
  street_address VARCHAR(50), 
  state VARCHAR(50),
  city VARCHAR(50),
  zipcode INT
);
CREATE TABLE IF NOT EXISTS conditions (
  condition_id INT PRIMARY KEY,
  name VARCHAR(50)
);
-- Add sample data. 
INSERT INTO test_table
  (name, color)
VALUES
  ('dev', 'blue'),
  ('pro', 'yellow'),
  ('junior', 'red');