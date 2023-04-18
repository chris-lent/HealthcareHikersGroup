from flask import Blueprint, request, jsonify, make_response
import json
from src import db


hospital_employee = Blueprint('hospital_employee', __name__)

# Get a patient’s (patient_id) current insurance plan (policy_id)
@hospital_employee.route('/patient/<patientID>', methods=['GET'])
def get_insurance(patientID):
    cursor = db.get_db().cursor()
    cursor.execute('''
        SELECT plan_name
        FROM insurance_plan ip JOIN
            (SELECT policy_id FROM patient
            WHERE patient_id = {0}) p USING(policy_id);
    '''.format(patientID))

    # grab the column headers from the returned data
    column_headers = [x[0] for x in cursor.description]

    # create an empty dictionary object to use in 
    # putting column headers together with data
    json_data = []

    # fetch all the data from the cursor
    theData = cursor.fetchall()
    
    # for each of the rows, zip the data elements together with
    # the column headers. 
    for row in theData:
        json_data.append(dict(zip(column_headers, row)))

    return jsonify(json_data)

@hospital_employee.route('/center_offers_services/{center_id}', methods=['POST'])
def add_new_service():

    # collecting the data from the request object
    the_data = request.json 
    current_app.logger.info(the_data)

    # extracting the variable
    name = the_data['product_name']
    description = the_data['product_description']
    price = the_data['product_price']
    category = the_data['product_category']

    # constructing the query
    query = 'insert into products (product_name, description, list_price) values ("'
    query += name + '", "'
    query += description + '", "'
    query += category + '", '
    query += str(price) + ')'
    current_app.logger.info(query)

    #executing and commiting the inset statement
    cursor = db.get_db().cursor()
    cursor.execute(query)
    db.get_db().commit()

    return "Success!"