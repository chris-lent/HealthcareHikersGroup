-- Create a new database.  You can change the name later.  You'll
-- need this name in the FLASK API file(s),  the AppSmith
-- data source creation.
create database if not exists dockter;

-- Via the Docker Compose file, a special user called webapp will
-- be created in MySQL. We are going to grant that user
-- all privileges to the new database we just created.
-- to change it here too.
grant all privileges on dockter.* to 'webapp'@'%';
flush privileges;

-- Move into the database we just created.
-- change it here too.
use dockter;

-- Put your DDL

CREATE TABLE IF NOT EXISTS medical_center (
  center_id INT PRIMARY KEY,
  center_name VARCHAR(50),
  street_address VARCHAR(50),
  state VARCHAR(2),
  city VARCHAR(50),
  zipcode INT,
  phone VARCHAR(10)
);

CREATE TABLE IF NOT EXISTS healthcare_admin_employee (
  admin_id INT PRIMARY KEY,
  first_name VARCHAR(20),
  last_name VARCHAR(20),
  center_id INT,
  FOREIGN KEY (center_id) references medical_center (center_id)
);

CREATE TABLE IF NOT EXISTS medical_professional (
  doc_id INT PRIMARY KEY,
  first_name VARCHAR(20),
  last_name VARCHAR(20),
  specialty_name VARCHAR(100),
  admin_id INT,
  FOREIGN KEY (admin_id) references healthcare_admin_employee (admin_id)
);

CREATE TABLE IF NOT EXISTS availability (
  doc_id INT,
  sched_id INT,
  day_of_week VARCHAR(3),
  start_time TIME,
  end_time TIME,
  PRIMARY KEY (doc_id, sched_id),
  FOREIGN KEY (doc_id) references medical_professional (doc_id)
);


CREATE TABLE IF NOT EXISTS insurance_company (
  company_id INT PRIMARY KEY,
  company_name VARCHAR(50)
);

CREATE TABLE IF NOT EXISTS insurance_plan (
  policy_id INT PRIMARY KEY,
  plan_name VARCHAR(500) NOT NULL,
  company_id INT,
  FOREIGN KEY (company_id) references insurance_company (company_id)
);

CREATE TABLE IF NOT EXISTS insurance_rep (
  insurance_rep_id INT PRIMARY KEY,
  first_name VARCHAR(20) NOT NULL,
  last_name VARCHAR(20) NOT NULL,
  company_id INT,
  FOREIGN KEY (company_id) references insurance_company (company_id)
);

CREATE TABLE IF NOT EXISTS patient (
  patient_id INT(11) NOT NULL,
  first_name VARCHAR(20) NOT NULL,
  middle_name VARCHAR(20) DEFAULT NULL,
  last_name VARCHAR(20) NOT NULL,
  phone VARCHAR(10) DEFAULT NULL,
  street_address VARCHAR(100) DEFAULT NULL,
  city VARCHAR(200) DEFAULT NULL,
  state VARCHAR(100) DEFAULT NULL,
  zipcode VARCHAR(50) DEFAULT NULL,
  policy_id INT(11) DEFAULT NULL,
  insurance_rep_id INT(11) DEFAULT NULL,
  PRIMARY KEY (patient_id),
  FOREIGN KEY (policy_id) REFERENCES insurance_plan (policy_id),
  FOREIGN KEY (insurance_rep_id) REFERENCES insurance_rep (insurance_rep_id)
);

CREATE TABLE IF NOT EXISTS appointment (
  appoint_id INT PRIMARY KEY,
  appoint_time TIME,
  appoint_date DATE,
  doc_id INT,
  patient_id INT,
  FOREIGN KEY (doc_id) references medical_professional (doc_id),
  FOREIGN KEY (patient_id) references patient (patient_id)
);

CREATE TABLE IF NOT EXISTS medical_history (
  record_id INT PRIMARY KEY,
  patient_id INT,
  FOREIGN KEY (patient_id) references patient (patient_id)
);

CREATE TABLE IF NOT EXISTS procedures (
    record_id INT,
    past_procedure VARCHAR(50),
    PRIMARY KEY (record_id, past_procedure),
    FOREIGN KEY (record_id) references medical_history (record_id)
);

CREATE TABLE IF NOT EXISTS immunizations (
    record_id INT,
    immunization_name VARCHAR(50),
    PRIMARY KEY (record_id, immunization_name),
    FOREIGN KEY (record_id) references medical_history (record_id)
);

CREATE TABLE IF NOT EXISTS medications (
    record_id INT,
    prescribed_medications VARCHAR(50),
    PRIMARY KEY (record_id, prescribed_medications),
    FOREIGN KEY (record_id) references medical_history (record_id)
);

CREATE TABLE IF NOT EXISTS allergies (
    record_id INT,
    allergy VARCHAR(50),
    PRIMARY KEY (record_id, allergy),
    FOREIGN KEY (record_id) references medical_history (record_id)
);


CREATE TABLE IF NOT EXISTS family_conditions (
    record_id INT,
    fam_condition VARCHAR(50),
    PRIMARY KEY (record_id, fam_condition),
    FOREIGN KEY (record_id) references medical_history (record_id)
);

CREATE TABLE IF NOT EXISTS conditions (
  condition_id INT PRIMARY KEY,
  condition_name VARCHAR(50)
);

CREATE TABLE IF NOT EXISTS services (
  service_id INT PRIMARY KEY,
  service_name VARCHAR(50)
);

-- Bridge Tables ---------------------------------------------------------

CREATE TABLE IF NOT EXISTS center_offers_services (
    center_id INT,
    service_id INT,
    PRIMARY KEY (center_id, service_id),
    FOREIGN KEY (center_id) references medical_center (center_id),
    FOREIGN KEY (service_id) references services (service_id)
);


CREATE TABLE IF NOT EXISTS center_accepts_insurance_plan (
    center_id INT,
    policy_id INT,
    PRIMARY KEY (center_id, policy_id),
    FOREIGN KEY (center_id) references medical_center (center_id),
    FOREIGN KEY (policy_id) references insurance_plan (policy_id)
);

CREATE TABLE IF NOT EXISTS center_contracts_insurance_comp (
    center_id INT,
    company_id INT,
    PRIMARY KEY (center_id, company_id),
    FOREIGN KEY (center_id) references medical_center (center_id),
    FOREIGN KEY (company_id) references insurance_company (company_id)
);

CREATE TABLE IF NOT EXISTS professional_specializes_service (
    service_id INT,
    doc_id INT,
    PRIMARY KEY (service_id, doc_id),
    FOREIGN KEY (service_id) references services (service_id),
    FOREIGN KEY (doc_id) references medical_professional (doc_id)
);

CREATE TABLE IF NOT EXISTS patient_has_condition (
    patient_id INT,
    condition_id INT,
    PRIMARY KEY (patient_id, condition_id),
    FOREIGN KEY (patient_id) references services (service_id),
    FOREIGN KEY (condition_id) references conditions (condition_id)
);

CREATE TABLE IF NOT EXISTS service_treats_condition (
    service_id INT,
    condition_id INT,
    PRIMARY KEY (service_id, condition_id),
    FOREIGN KEY (service_id) references services (service_id),
    FOREIGN KEY (condition_id) references conditions (condition_id)
);


CREATE TABLE IF NOT EXISTS insurance_covers_service (
    service_id INT,
    policy_id INT,
    referral_needed BOOLEAN,
    coverage_description VARCHAR(50),
    PRIMARY KEY (service_id, policy_id),
    FOREIGN KEY (service_id) references services (service_id),
    FOREIGN KEY (policy_id) references insurance_plan (policy_id)
);


-- INSERT DATA ---------------------------------------------------------
INSERT INTO medical_center (center_id, center_name, street_address, state, city, zipcode, phone)
VALUES (1, 'Bringham', '1 ABC Street', 'MA', 'Boston', 02120, '6171234789');
INSERT INTO medical_center (center_id, center_name, street_address, state, city, zipcode, phone)
VALUES (2, 'Mass Gen', '1 State Street', 'MA', 'Boston', 02120, '6173333333');

INSERT INTO healthcare_admin_employee (admin_id, first_name, last_name, position, center_id)
VALUES (1, 'John', 'Smith', 2);
INSERT INTO healthcare_admin_employee (admin_id, first_name, last_name, position, center_id)
VALUES (2, 'Jill', 'Barnes', 1);

INSERT INTO medical_professional (doc_id, first_name, last_name, specialty_name, admin_id)
VALUES (1, 'Amy', 'Lake', 'Dermatology', 1);
INSERT INTO medical_professional (doc_id, first_name, last_name, specialty_name, admin_id)
VALUES (2, 'Ally', 'Jones', 'Oncology', 2);

INSERT INTO availability (doc_id, sched_id, day_of_week, start_time, end_time)
VALUES (1, 1, 'WED', '10:00:00', '11:00:00');
INSERT INTO availability (doc_id, sched_id, day_of_week, start_time, end_time)
VALUES (1, 2, 'TUE', '12:00:00', '13:00:00');
INSERT INTO availability (doc_id, sched_id, day_of_week, start_time, end_time)
VALUES (2, 3, 'TUE', '12:00:00', '13:00:00');

INSERT INTO insurance_company (company_id, company_name)
VALUES (1, 'Blue Cross Blue Shield');
INSERT INTO insurance_company (company_id, company_name)
VALUES (2, 'Health New England');

INSERT INTO insurance_plan (policy_id, plan_name, company_id)
VALUES (1, 'Federal Employee Program', 1);
INSERT INTO insurance_plan (policy_id, plan_name, company_id)
VALUES (2, 'Student Program', 2);

INSERT INTO insurance_rep (insurance_rep_id, first_name, last_name, company_id)
VALUES (1, 'Jane', 'Smith', 2);
INSERT INTO insurance_rep (insurance_rep_id, first_name, last_name, company_id)
VALUES (2, 'Jill', 'Baker', 1);

INSERT INTO patient (patient_id, first_name, middle_name, last_name, phone, street_address, city, state, zipcode,
                     policy_id, insurance_rep_id)
VALUES (1, 'Jake', 'Brad', 'Smith', '5162222222', '1 Lane Street', 'Boston', 'MA', 02115, 1, 2);
INSERT INTO patient (patient_id, first_name, middle_name, last_name, phone, street_address, city, state, zipcode,
                     policy_id, insurance_rep_id)
VALUES (2, 'John', 'Brandon', 'Baker', '5162223333', '12 Brick Road', 'Brookline', 'MA', 02445, 2, 1);

INSERT INTO appointment (appoint_id, appoint_time, appoint_date, doc_id, patient_id)
VALUES (1, '10:00:00', 2023-04-12, 1, 1);
INSERT INTO appointment (appoint_id, appoint_time, appoint_date, doc_id, patient_id)
VALUES (2, '12:00:00', 2023-04-11, 2, 1);

INSERT INTO medical_history (record_id, patient_id)
VALUES (1, 1);
INSERT INTO medical_history (record_id, patient_id)
VALUES (2, 2);

INSERT INTO procedures (record_id, past_procedure)
VALUES (1, 'Back surgery');
INSERT INTO procedures (record_id, past_procedure)
VALUES (1, 'Neck surgery');

INSERT INTO immunizations (record_id, immunization_name)
VALUES (1, 'Chicken Pox');
INSERT INTO immunizations (record_id, immunization_name)
VALUES (2, 'Covid-19');

INSERT INTO medications (record_id, prescribed_medications)
VALUES (1, 'Zoloft');
INSERT INTO medications (record_id, prescribed_medications)
VALUES (1, 'Xanax');

INSERT INTO allergies (record_id, allergy)
VALUES (1, 'Peanuts');
INSERT INTO allergies (record_id, allergy)
VALUES (2, 'Shellfish');

INSERT INTO family_conditions (record_id, fam_condition)
VALUES (1, 'Dementia');
INSERT INTO family_conditions (record_id, fam_condition)
VALUES (2, 'Cancer');

INSERT INTO conditions (condition_id, condition_name)
VALUES (1, 'Hormonal Acne');
INSERT INTO conditions (condition_id, condition_name)
VALUES (2, 'Skin Cancer');

INSERT INTO services (service_id, service_name)
VALUES (1, 'X-Ray');
INSERT INTO services (service_id, service_name)
VALUES (2, 'Surgery');

INSERT INTO center_offers_services(service_id, center_id)
VALUES (1, 1);
INSERT INTO center_offers_services (service_id, center_id)
VALUES (2, 2);

INSERT INTO center_accepts_insurance_plan(policy_id, center_id)
VALUES (1, 1);
INSERT INTO center_accepts_insurance_plan(policy_id, center_id)
VALUES (2, 1);


INSERT INTO center_contracts_insurance_comp(company_id, center_id)
VALUES (1, 1);
INSERT INTO center_contracts_insurance_comp(company_id, center_id)
VALUES (2, 2);

INSERT INTO professional_specializes_service(service_id, doc_id)
VALUES (1, 1);
INSERT INTO professional_specializes_service(service_id, doc_id)
VALUES (2, 2);

INSERT INTO patient_has_condition(patient_id, condition_id)
VALUES (1, 1);
INSERT INTO patient_has_condition(patient_id, condition_id)
VALUES (2, 2);

INSERT INTO service_treats_condition(service_id, condition_id)
VALUES (1, 1);
INSERT INTO service_treats_condition(service_id, condition_id)
VALUES (2, 2);

INSERT INTO insurance_covers_service(service_id, policy_id, referral_needed, coverage_description)
VALUES (1, 1, True, 'Partial Coverage');
INSERT INTO insurance_covers_service(service_id, policy_id, referral_needed, coverage_description)
VALUES (2, 2, False, 'Full Coverage');


