from flask import Blueprint, request, jsonify, make_response, current_app
import json
from src import db


hospital_employee = Blueprint('hospital_employee', __name__)

# Get a patient’s (patient_id) current insurance plan (policy_id)
@hospital_employee.route('/patient', methods=['GET'])
def get_insurance():
    # collecting the data from the request object
    the_data = request.json 
    current_app.logger.info(the_data)

    # extracting the variable
    patientID = the_data['patient_id']

    cursor = db.get_db().cursor()
    cursor.execute('''
        SELECT company_name, policy_id, plan_name
        FROM insurance_company JOIN
            (insurance_plan ip JOIN
            (SELECT policy_id FROM patient
            WHERE patient_id = {0}) p USING(policy_id)) USING (company_id);
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

# Add services the center offers
@hospital_employee.route('/center_offers_services/<centerID>', methods=['POST'])
def center_add_new_service(centerID):

    # collecting the data from the request object
    the_data = request.json 
    current_app.logger.info(the_data)

    # extracting the variable
    serviceCode = the_data['service_id']

    # constructing the query
    query = 'insert into center_offers_services values ({0},{1})'.format(centerID, serviceCode)
    current_app.logger.info(query)

    #executing and commiting the inset statement
    cursor = db.get_db().cursor()
    cursor.execute(query)
    db.get_db().commit()

    return "Success!"

# Delete services the center offers
@hospital_employee.route('/center_offers_services/<centerID>', methods=['DELETE'])
def center_delete_service(centerID):

    # collecting the data from the request object
    the_data = request.json 
    current_app.logger.info(the_data)

    # extracting the variable
    serviceCode = the_data['service_id']

    # constructing the query
    query = '''
        DELETE FROM center_offers_services 
        WHERE center_id = {0} AND service_id = {1}
    '''.format(centerID, serviceCode)

    current_app.logger.info(query)

    #executing and commiting the inset statement
    cursor = db.get_db().cursor()
    cursor.execute(query)
    db.get_db().commit()

    return "Success!"

# Updates doctor's avalibility
@hospital_employee.route('/availibility', methods=['PUT'])
def update_avalibility():

    # collecting the data from the request object
    the_data = request.json 
    current_app.logger.info(the_data)

    # extracting the variable
    # schedID = the_data['sched_id']
    docID = the_data['doc_id']
    schedID = the_data['sched_id']
    day = the_data['day_of_week']
    start = the_data['start_time']
    end = the_data['end_time']

    # constructing the query
    query = '''
        UPDATE availability 
        SET day_of_week = '{}', start_time = '{}', end_time = '{}' 
        WHERE doc_id = {} AND sched_id = {};
    '''.format(day, start, end, docID, schedID)

    current_app.logger.info(query)

    #executing and commiting the inset statement
    cursor = db.get_db().cursor()
    cursor.execute(query)
    db.get_db().commit()

    return "Success!"

# Add medical center's accepted insurance plan
@hospital_employee.route('/center_accepts_insurance_plan/<centerID>', methods=['POST'])
def add_new_insurance(centerID):

    # collecting the data from the request object
    the_data = request.json 
    current_app.logger.info(the_data)

    # extracting the variable
    policyID = the_data['policy_id']

    # constructing the query
    query = 'insert into center_accepts_insurance_plan values ({0},{1})'.format(centerID, policyID)
    current_app.logger.info(query)

    #executing and commiting the inset statement
    cursor = db.get_db().cursor()
    cursor.execute(query)
    db.get_db().commit()

    return "Success!"

# Delete medical center's accepted insurance plans
@hospital_employee.route('/center_accepts_insurance_plan/<centerID>', methods=['DELETE'])
def delete_insurance(centerID):

    # collecting the data from the request object
    the_data = request.json 
    current_app.logger.info(the_data)

    # extracting the variable
    policyID = the_data['policy_id']

    # constructing the query
    query = '''
        DELETE FROM center_accepts_insurance_plan 
        WHERE center_id = {0} AND policy_id = {1}
    '''.format(centerID, policyID)

    current_app.logger.info(query)

    #executing and commiting the inset statement
    cursor = db.get_db().cursor()
    cursor.execute(query)
    db.get_db().commit()

    return "Success!"

# Get insurance plans accepted at a medical center
@hospital_employee.route('/insurance_plans_accepted/<centerID>', methods=['GET'])
def accepted_insurances(centerID):
    # get a cursor object from the database
    cursor = db.get_db().cursor()

    # use cursor to query the database for a list of products
    cursor.execute('''
        SELECT company_name, policy_id, plan_name
        FROM insurance_company JOIN
            (insurance_plan ip JOIN
            (SELECT policy_id FROM center_accepts_insurance_plan
            WHERE center_id = {0}) p USING(policy_id)) USING (company_id);
    '''.format(centerID))

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

# Add new services a medical professional offers
@hospital_employee.route('/professional_specializes_service/<docID>', methods=['POST'])
def add_new_services(docID):

    # collecting the data from the request object
    the_data = request.json 
    current_app.logger.info(the_data)

    # extracting the variable
    serviceID = the_data['service_id']

    # constructing the query
    query = 'insert into professional_specializes_service values ({0},{1})'.format(serviceID, docID)
    current_app.logger.info(query)

    #executing and commiting the inset statement
    cursor = db.get_db().cursor()
    cursor.execute(query)
    db.get_db().commit()

    return "Success!"

# Delete services a medical professional offers
@hospital_employee.route('/professional_specializes_service/<docID>', methods=['DELETE'])
def delete_services(docID):

    # collecting the data from the request object
    the_data = request.json 
    current_app.logger.info(the_data)

    # extracting the variable
    serviceID = the_data['service_id']

    # constructing the query
    query = '''
        DELETE FROM professional_specializes_service 
        WHERE doc_id = {0} AND service_id = {1}
    '''.format(docID, serviceID)

    current_app.logger.info(query)

    #executing and commiting the inset statement
    cursor = db.get_db().cursor()
    cursor.execute(query)
    db.get_db().commit()

    return "Success!"