from flask import Flask, request, jsonify
from os import environ, remove, getenv 
import logging
import json
from datetime import datetime

webhook = Flask(__name__)

webhook.logger.setLevel(logging.INFO)

# Simple route to make sure the admission controller is alive
@webhook.route('/check', methods=['GET'])
def hello():
    return "<h1 style='color:blue'>Ready!</h1>"

# Our validation route to receive the webhook request.  We'll use this in our Admission Controller K8s manifest
@webhook.route('/validate', methods=['POST'])
def validating_webhook():
    request_info = request.get_json()
    uid = request_info["request"].get("uid")
    object = f'{request_info["request"]["object"]["kind"]}/{request_info["request"]["object"]["metadata"]["name"]}'

    # To see the requests and create rules to start we will save the request to a file.  We can delete this for prod
    with open(uid, 'w') as file:
        file.write(request_info)

### Lets check the scheme of the object for something we can deny access on!  Perhaps check for privileged flag in the SecurityContext or using the 'latest" as an image tag

    # Set a default of everything is allowed
    result = False
# Your code goes here


### Set the variable called 'result' of the check to True if the object passes and False if we should BLOCK the object from becoming persistent

    if result == True:

        response = f"\nAC Workshop cleared object {object} as compliant with admission policy.\n"
        webhook.logger.info(f'Object {object} passed security checks. Allowing the request.')

    else:
        response = f"\nAC Workshop found the object {object} in violation of admission policy.\n"
        webhook.logger.error(f'Object {object} failed security checks. Request rejected!')

    return admission_response(result, uid, response)

def admission_response(allowed, uid, message):
    return jsonify({"apiVersion": "admission.k8s.io/v1",
                    "kind": "AdmissionReview",
                    "response": {
                         "allowed": allowed,
                         "uid": uid,
                         "status": {
                           "code": 403,
                           "message": message
                         }
                       }
                    })


if __name__ == '__main__':
    webhook.run(host='0.0.0.0', port=1701)
