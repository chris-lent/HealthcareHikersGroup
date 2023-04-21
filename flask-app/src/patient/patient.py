from flask import Blueprint, request, jsonify, make_response, current_app
from datetime import timedelta
import json
from src import db

patient = Blueprint('patient', __name__)

# GET request that retrieves all the treatment centers that support a 
# patient's insurance plan, given the policy_id parameter
@patient.route('/medical_center_insurance', methods=['GET'])
def get_medical_centers_with_insurance_plan():
    print("Endpoint called!")
    # collecting the data from the request object
    the_data = request.json 
    current_app.logger.info(the_data)

    # extracting the variable
    patientID = the_data["patient_id"]
    cursor = db.get_db().cursor()
    cursor.execute(''' SELECT center_name, street_address, city, state, zipcode FROM medical_center 
                        JOIN center_accepts_insurance_plan ip on medical_center.center_id = ip.center_id
                        JOIN (SELECT policy_id from patient
                        WHERE patient_id = {0}) as p where p.policy_id = ip.policy_id
                        '''.format(patientID))

    # grab the column headers from the returned data
    row_headers = [x[0] for x in cursor.description]
    results = cursor.fetchall()
    json_data = []
    for result in results:
        json_data.append(dict(zip(row_headers, result)))
    response = make_response(jsonify(json_data))
    response.status_code = 200
    response.mimetype = 'application/json'
    return response

    
#Return all treatment centers (center_id) that have a specific 
#specialization {service_id}

@patient.route('/medical_center_service', methods=['GET'])
def get_medical_centers_with_service():
    # collecting the data from the request object
    the_data = request.json 
    current_app.logger.info(the_data)

    # extracting the variable
    serviceName = the_data["serviceName"]
    cursor = db.get_db().cursor()
    cursor.execute(''' select center_name ,street_address, city, state, zipcode from medical_center mc
                    join center_offers_services cos on mc.center_id = cos.center_id
                    join (select * from services where service_name = "{0}")
                    as s where cos.service_id = s.service_id'''.format(serviceName))

    # grab the column headers from the returned data
    row_headers = [x[0] for x in cursor.description]
    results = cursor.fetchall()
    json_data = []
    for result in results:
        json_data.append(dict(zip(row_headers, result)))
    response = make_response(jsonify(json_data))
    response.status_code = 200
    response.mimetype = 'application/json'
    return response

# Getting the location based on the patients location
@patient.route('/medical_center_location', methods=['GET'])
def get_closest_medical_centers():
    print("Endpoint called!")
    cursor = db.get_db().cursor()
    # collecting the data from the request object
    the_data = request.json 
    current_app.logger.info(the_data)

    # extracting the variable
    patientID = the_data["patientID"]
    cursor.execute(''' SELECT center_name, mc.street_address, mc.city, mc.state, mc.zipcode from medical_center mc
                       JOIN (select city from patient where patient_id={0}) 
                       as p where mc.city = p.city'''.format(patientID))

    # grab the column headers from the returned data
    row_headers = [x[0] for x in cursor.description]
    results = cursor.fetchall()
    json_data = []
    for result in results:
        json_data.append(dict(zip(row_headers, result)))
    response = make_response(jsonify(json_data))
    response.status_code = 200
    response.mimetype = 'application/json'
    return response

# Return availability for a {doc_id} with a specific specialty  {specialty_name)
@patient.route('/doc_availability_by_service', methods=['GET'])
def get_doc_availability():
    print("Endpoint called!")
    cursor = db.get_db().cursor()
    # collecting the data from the request object
    the_data = request.json 
    current_app.logger.info(the_data)

    # extracting the variable
    serviceName = the_data["serviceName"]
    cursor.execute(''' SELECT mp.first_name, mp.last_name, mc.center_name, street_address, city, state, zipcode, day_of_week, start_time, end_time 
                       FROM availability a
                       JOIN medical_professional AS mp ON a.doc_id = mp.doc_id
                       JOIN professional_specializes_service pss on mp.doc_id = pss.doc_id
                       JOIN (select * from services where service_name = "{0}")
                       AS s on pss.service_id = s.service_id
                       JOIN center_offers_services AS cos on s.service_id = cos.service_id
                       JOIN medical_center AS mc ON cos.center_id = mc.center_id'''.format(serviceName))

    # grab the column headers from the returned data
    row_headers = [x[0] for x in cursor.description]
    results = cursor.fetchall()
    json_data = []
    for result in results:
        start_time_str = str(result[8])
        end_time_str = str(result[9])

        # Include the strings in the JSON data
        result_dict = {
            'first_name': result[0],
            'last_name': result[1],
            'center_name': result[2],
            'street_address': result[3],
            'city': result[4],
            'state': result[5],
            'zipcode': result[6],
            'day_of_week': result[7],
            'start_time': start_time_str,
            'end_time': end_time_str
        }

        # Append the modified result to the JSON data list
        json_data.append(result_dict)
    response = make_response(jsonify(json_data))
    response.status_code = 200
    response.mimetype = 'application/json'
    return response  

# Return patient medication.
@patient.route('/get_patient_medications', methods=['GET'])
def get_patient_medications():
    print("Endpoint called!")
    cursor = db.get_db().cursor()
    # collecting the data from the request object
    the_data = request.json 
    current_app.logger.info(the_data)

    # extracting the variable
    patientID = the_data["patientID"]
    cursor.execute(''' select prescribed_medications from patient p
                    join medical_history mh on p.record_id = mh.record_id
                    join medications m on mh.record_id = m.record_id
                    where patient_id = {0}
                        '''.format(patientID))

    # grab the column headers from the returned data
    row_headers = [x[0] for x in cursor.description]
    results = cursor.fetchall()
    json_data = []
    for result in results:
        json_data.append(dict(zip(row_headers, result)))
    response = make_response(jsonify(json_data))
    response.status_code = 200
    response.mimetype = 'application/json'
    return response

# Return patient allergy.
@patient.route('/get_patient_allergies', methods=['GET'])
def get_patient_allergies():
    print("Endpoint called!")
    cursor = db.get_db().cursor()
    # collecting the data from the request object
    the_data = request.json 
    current_app.logger.info(the_data)

    # extracting the variable
    patientID = the_data["patientID"]
    cursor.execute(''' select allergy from patient p
                    join medical_history mh on p.record_id = mh.record_id
                    join allergies a on mh.record_id = a.record_id
                    where patient_id = {0}
                        '''.format(patientID))

    # grab the column headers from the returned data
    row_headers = [x[0] for x in cursor.description]
    results = cursor.fetchall()
    json_data = []
    for result in results:
        json_data.append(dict(zip(row_headers, result)))
    response = make_response(jsonify(json_data))
    response.status_code = 200
    response.mimetype = 'application/json'
    return response

# Update patient contact information
@patient.route('/update_contact_info', methods=['PUT'])
def update_contact_info():
    print("Endpoint called!")
    # collecting the data from the request object
    the_data = request.json 
    current_app.logger.info(the_data)
    patientID = the_data.get('patientID')
    phone = the_data.get('phone')

    query = '''
        UPDATE patient
        SET phone = '{1}' WHERE patient_id = {0}
    '''.format(patientID, phone)

    current_app.logger.info(query)

    #executing and commiting the update statement
    cursor = db.get_db().cursor()
    cursor.execute(query)
    db.get_db().commit()

    return "Success!"
    
# Return patient phone number.
@patient.route('/get_patient_phone_num', methods=['GET'])
def get_patient_phone_num():
    print("Endpoint called!")
    cursor = db.get_db().cursor()
    # collecting the data from the request object
    the_data = request.json 
    current_app.logger.info(the_data)

    # extracting the variable
    patientID = the_data["patientID"]
    cursor.execute(''' select phone from patient
                        where patient_id = "{0}"
                        '''.format(patientID))

    # grab the column headers from the returned data
    row_headers = [x[0] for x in cursor.description]
    results = cursor.fetchall()
    json_data = []
    for result in results:
        json_data.append(dict(zip(row_headers, result)))
    response = make_response(jsonify(json_data))
    response.status_code = 200
    response.mimetype = 'application/json'
    return response

# Input patient allergy.
@patient.route('/input_patient_allergies', methods=['POST'])
def input_patient_allergies():

    # collecting the data from the request object
    the_data = request.json 
    current_app.logger.info(the_data)
    # extracting the variable
    recordID = the_data.get('recordID')
    allergy = the_data.get('allergy')

    # constructing the query
    query = 'insert into allergies values ({0},"{1}")'.format(recordID, allergy)
    current_app.logger.info(query)

    #executing and commiting the inset statement
    cursor = db.get_db().cursor()
    cursor.execute(query)
    db.get_db().commit()

    return "Success!"

    
# Delete patient allergy.
@patient.route('/delete_patient_allergy', methods=['DELETE'])
def delete_patient_allergy():

    # collecting the data from the request object
    the_data = request.json 
    current_app.logger.info(the_data)

    # extracting the variable
    allergy = the_data.get('allergy')
    recordID = the_data.get('recordID')

    # constructing the query
    query = '''
        DELETE FROM allergies 
        WHERE record_id = {0} AND allergy = "{1}"
    '''.format(recordID, allergy)

    current_app.logger.info(query)

    #executing and commiting the inset statement
    cursor = db.get_db().cursor()
    cursor.execute(query)
    db.get_db().commit()

    return "Success!"


# Input patient medication.
@patient.route('/input_patient_medication', methods=['POST'])
def input_patient_medication():

    # collecting the data from the request object
    the_data = request.json 
    current_app.logger.info(the_data)
    # extracting the variable
    recordID = the_data.get('recordID')
    medication = the_data.get('medication')

    # constructing the query
    query = 'insert into medications values ({0},"{1}")'.format(recordID, medication)
    current_app.logger.info(query)

    #executing and commiting the inset statement
    cursor = db.get_db().cursor()
    cursor.execute(query)
    db.get_db().commit()

    return "Success!"

# Delete patient medication.
@patient.route('/delete_patient_medication', methods=['DELETE'])
def delete_patient_medication():

    # collecting the data from the request object
    the_data = request.json 
    current_app.logger.info(the_data)

    # extracting the variable
    medication = the_data.get('medication')
    recordID = the_data.get('recordID')

    # constructing the query
    query = '''
        DELETE FROM medications 
        WHERE record_id = {0} AND prescribed_medications = "{1}"
    '''.format(recordID, medication)

    current_app.logger.info(query)

    #executing and commiting the inset statement
    cursor = db.get_db().cursor()
    cursor.execute(query)
    db.get_db().commit()

    return "Success!"