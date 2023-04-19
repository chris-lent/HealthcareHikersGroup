from flask import Blueprint, request, jsonify, make_response
import json
from src import db

patient = Blueprint('patient', __name__)

# Get all patients from the DB
@patient.route('/patient', methods=['GET'])
def get_patients():
    cursor = db.get_db().cursor()
    cursor.execute('SELECT * FROM patient')
    row_headers = [x[0] for x in cursor.description]
    results = cursor.fetchall()
    json_data = []
    for result in results:
        json_data.append(dict(zip(row_headers, result)))
    response = make_response(jsonify(json_data))
    response.status_code = 200
    response.mimetype = 'application/json'
    return response


# GET request that retrieves all the treatment centers that support a 
# patient's insurance plan, given the policy_id parameter

medical_centers = Blueprint('medical_centers', __name__)
@patient.route('/medical_centers/<patientID>', methods=['GET'])
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

    #@patient.route('/medical_center/<center>', methods = ['GET'])
    #def get_medical_centers_with_service():
        #query = '''

        #'''

     #centers = db.session.query(MedicalCenter).all()
     #result = []
     #for center in centers:
         #center_data = {
            #'center_id': center.center_id,
            # 'center_name': center.center_name,
             #'street_address': center.street_address,
             #'state': center.state,
            # 'city': center.city,
            # 'zipcode': center.zipcode,
            # 'phone': center.phone
         #}

#         # Get the services offered by the center
#         services = db.session.query(Service).join(CenterOffersService).filter(CenterOffersService.center_id == center.center_id).all()
#         services_data = []
#         for service in services:
#             services_data.append({
#                 'service_id': service.service_id,
#                 'service_name': service.service_name
#             })
#         center_data['services'] = services_data
#         # Get the insurance plans accepted by the center
#         insurance_plans = db.session.query(InsurancePlan).join(CenterAcceptsInsurancePlan).filter(CenterAcceptsInsurancePlan.center_id == center.center_id).all()
#         insurance_plans_data = []
#         for plan in insurance_plans:
#             insurance_plans_data.append({
#                 'policy_id': plan.policy_id,
#                 'plan_name': plan.plan_name,
#                 'company_id': plan.company_id
#             })
#         center_data['insurance_plans'] = insurance_plans_data
#         result.append(center_data)
#     return jsonify(result)

    