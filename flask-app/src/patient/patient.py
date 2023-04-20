from flask import Blueprint, request, jsonify, make_response, current_app
from datetime import timedelta
import json
from src import db

patient = Blueprint('patient', __name__)

# GET request that retrieves all the treatment centers that support a 
# patient's insurance plan, given the policy_id parameter
@patient.route('/medical_center_insurance/<patientID>', methods=['GET'])
def get_medical_centers_with_insurance_plan(patientID):
    print("Endpoint called!")
    cursor = db.get_db().cursor()
    cursor.execute(''' SELECT center_name FROM medical_center 
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
medical_centers = Blueprint('medical_centers', __name__)
@patient.route('/medical_center_service/<serviceID>', methods=['GET'])
def get_medical_centers_with_service(serviceID):
    print("Endpoint called!")
    cursor = db.get_db().cursor()
    cursor.execute(''' select center_name from medical_center mc
                        JOIN (select * from center_offers_services WHERE service_id = {0})
                         as cos WHERE mc.center_id = cos.center_id'''.format(serviceID))

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
@patient.route('/medical_center_location/<patientID>', methods=['GET'])
def get_closest_medical_centers(patientID):
    print("Endpoint called!")
    cursor = db.get_db().cursor()
    cursor.execute(''' SELECT center_name from medical_center mc
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
@patient.route('/doc_availability_by_service/<serviceID>', methods=['GET'])
def get_doc_availability(serviceID):
    print("Endpoint called!")
    cursor = db.get_db().cursor()
    cursor.execute(''' SELECT a.doc_id, day_of_week, start_time, end_time 
                       FROM availability a
                       JOIN medical_professional AS mp ON a.doc_id = mp.doc_id
                       JOIN (SELECT doc_id FROM professional_specializes_service 
                       WHERE service_id={0}) pos ON mp.doc_id = pos.doc_id
    '''.format(serviceID))

    # grab the column headers from the returned data
    row_headers = [x[0] for x in cursor.description]
    results = cursor.fetchall()
    json_data = []
    for result in results:
        start_time_str = str(result[2])
        end_time_str = str(result[3])

        # Include the strings in the JSON data
        result_dict = {
            'doc_id': result[0],
            'day_of_week': result[1],
            'start_time': start_time_str,
            'end_time': end_time_str
        }

        # Append the modified result to the JSON data list
        json_data.append(result_dict)
    response = make_response(jsonify(json_data))
    response.status_code = 200
    response.mimetype = 'application/json'
    return response 


# Return patient medical history.
@patient.route('/medical_history/<patientID>', methods=['GET'])
def get_patient_history(patientID):
    print("Endpoint called!")
    cursor = db.get_db().cursor()
    cursor.execute(''' select patient_id,immunization_name, prescribed_medications,
                       fam_condition, past_procedure, allergy FROM medical_history mh
                       LEFT JOIN immunizations AS i ON mh.record_id = i.record_id
                       LEFT JOIN medications AS m ON mh.record_id = m.record_id
                       LEFT JOIN family_conditions AS fc ON mh.record_id = fc.record_id
                       LEFT JOIN procedures AS pr ON mh.record_id = pr.record_id
                       LEFT JOIN allergies AS a ON mh.record_id = a.record_id
                       WHERE patient_id = {0}
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
@patient.route('/update_contact_info/<int:patientID>-<phone>', methods=['PUT'])
def update_contact_info(patientID, phone):
    print("Endpoint called!")
    # collecting the data from the request object
    the_data = request.json 
    current_app.logger.info(the_data)

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


# Input patient contact information.
@patient.route('/input_contact_info/<patientID>', methods=['POST'])
def input_patient_contact_info(patientID):
    print("Endpoint called!")
    data = request.get_json()
    phone_number = data.get('phone_number')
    
    cursor = db.get_db().cursor()
    cursor.execute('UPDATE patient SET phone = ? WHERE patient_id = ?', 
                   (phone_number, patientID))
    db.get_db().commit()
    
    response = make_response(jsonify({'message': 'Patient phoe number updated.'}))
    response.status_code = 200
    response.mimetype = 'application/json'
    return response

# Input patient allergy.
@patient.route('/input_patient_allergies/<recordID>', methods=['POST'])
def input_patient_allergies(recordID):
    print("Endpoint called!")
    data = request.json
    allergies = data['allergies']

    cursor = db.get_db().cursor()
    for allergy in allergies:
        cursor.execute('INSERT INTO allergies (record_id, allergy) VALUES (?, ?)', (recordID, allergy))
    db.get_db().commit()

    response = make_response(jsonify({'message': 'Patient allergies added successfully.'}))
    response.status_code = 200
    response.mimetype = 'application/json'
    return response


# Delete patient phone number.
@patient.route('/delete_patient_phone/<patientID>', methods=['DELETE'])
def delete_patient_phone(patientID):
    print("Endpoint called!")
    cursor = db.get_db().cursor()
    cursor.execute('UPDATE patient SET phone = NULL WHERE patient_id = ?', (patientID,))
    db.get_db().commit()
    
    response = make_response(jsonify({'message': 'Patient phone number deleted.'}))
    response.status_code = 200
    response.mimetype = 'application/json'
    return response
