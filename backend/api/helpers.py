from functools import wraps
from flask import jsonify, request
from config import DEBUG

GENERIC_ERROR = 'Our bad - please contact support for further assistance'

def all_helper():
    return None

def requires_json(func):
    @wraps(func)
    def wrapper():
        body = request.json
        if (body == None):
            response = {'success': False, 'message': GENERIC_ERROR}
            if (DEBUG): response['message'] = 'Request body missing'
            return jsonify(response)
            
        return func(**body), 400
    return wrapper
    
def validate_types(expected):
    def _validate_types(func):
        @wraps(func)
        def wrapper(*args, **body):
            # Check each type and add to invalid if not correct
            invalid = {}
            for key, type in expected.items():
                if (not isinstance(body[key], type)):
                    invalid[key] = type
            
            # if there's any invalid fields, respond with an error
            if (len(invalid) > 0):
                response = {'success': False, 'message': GENERIC_ERROR}
                if (DEBUG):
                    response['message'] = ''
                    for key, type in invalid.items():
                        response['message'] += '\'{0}\' was expected to be a {1}, '.format(key, type.__name__)
                
                return jsonify(response), 400

            return func(**body)
        return wrapper
    return _validate_types