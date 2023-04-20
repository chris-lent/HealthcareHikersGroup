# Dock-ter App
## Description
This app is meant to streamline the process of connecting patients to medical professionals based on their insurance coverage and/or medical concerns.
The purpose of this app is to allow patients to search for treatment centers based on their insurance, location, medical concern, and availability. It will allow patients to directly access information about what services a doctor's office provides and whether those services would be covered by their insurance.  They can also find out other information about their insurance plan coverage like which specialists they would need a referral to see.

Additionally, it will allow healthcare employees to access information about patient's insurance plan, insurance plans accepted, doctor's availability, services offered at a center, and what services each doctor performs. The employee can adjust information on insurance plans accepted, doctor's availability, services offered and services performed by each doctor.

## Repository Structure
This repo contains a boilerplate setup for spinning up 3 Docker containers: 
1. A MySQL 8 container 
1. A Python Flask container to implement a REST API
1. A Local AppSmith Server

The `docker-compose.yml` file will create these containers.  

Inside the `db/` folder there is a `dockter_db_bootstrap.sql` file for creating the database and a `dockter_db_data.sql` for adding in the data. The SQL container will contain this database and its data.

Inside the `flask-app/` folder there is a `src` folder which contains the blueprints, a `Dockerfile` for simple python and an `app.py` file to create the app. Inside the `src` folder there is the `__init__.py` file which contains the function to create the app. In each folder `hospital_employee` and `patient` there is a corresponding python file of the same name. Each python file contains the routes for each persona in order to carry out the functions listed in the description above.

Inside the `thunder-tests/` folder are the json files which keep track of the thunder tests made for the blueprints in our repository.

The `secrets/` folder is empty, files will need to be added once the repository is cloned locally, this will be explained in the next section.

## How to setup and start the containers
1. Clone this repository.  
1. Create a file named `db_root_password.txt` in the `secrets/` folder and put inside of it the root password for MySQL. 
1. Create a file named `db_password.txt` in the `secrets/` folder and put inside of it the password you want to use for the a non-root user named webapp. 
1. In a terminal or command prompt, navigate to the folder with the `docker-compose.yml` file.  
1. Build the images with `docker compose build`
1. Start the containers with `docker compose up`.  To run in detached mode, run `docker compose up -d`. 

## Collaborators

## Notes







