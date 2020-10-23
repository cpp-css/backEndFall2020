from functools import wraps
import re
from flask import jsonify, request
from config import DEBUG, db
from database.session import Session
from database.user import User

GENERIC_ERROR = 'Our bad - please contact support for further assistance'

def all_helper():
    return None

def requires_auth(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        raw_auth = request.headers.get('Authorization')
        if (raw_auth == None):
            response = {'success': False, 'message': GENERIC_ERROR}
            if (DEBUG): response['message'] = 'Authorization header missing'
            return jsonify(response), 400
        
        auth = re.search("Bearer (.*)", raw_auth)
        if (auth == None):
            response = {'success': False, 'message': GENERIC_ERROR}
            if (DEBUG): response['message'] = 'Unsupported authorization type'
            return jsonify(response), 400
            
        session_id = auth.group(1)
        session = db.session.query(Session).filter(Session.session_id == session_id).limit(1).first()
        
        if (session == None or session.is_expired()):
            response = {'success': False, 'message': 'Please login again'}
            if (DEBUG): response['message'] = 'Session key expired or does not exist'
            return jsonify(response), 401
            
        request.session = session
        request.user = session.user
        return func(*args, **kwargs)
    return wrapper

def requires_json(func):
    @wraps(func)
    def wrapper():
        body = request.json
        if (body == None):
            response = {'success': False, 'message': GENERIC_ERROR}
            if (DEBUG): response['message'] = 'Request body missing'
            return jsonify(response), 400
            
        return func(**body)
    return wrapper
    
def validate_types(expected):
    def _validate_types(func):
        @wraps(func)
        def wrapper(*args, **body):
            # Check each type and add to invalid if not correct
            invalid = {}
            for key, type in expected.items():
                if (not key in body or not isinstance(body[key], type)):
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
