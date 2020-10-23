from functools import wraps
import re
from flask import abort, jsonify, request

from config import DEBUG, db
from database.session import Session
from database.user import User

def all_helper():
    return None

def requires_auth(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        raw_auth = request.headers.get('Authorization')
        if (raw_auth == None):
            abort(400, {'debug': 'Authorization header missing'})
        
        auth = re.search("Bearer (.*)", raw_auth)
        if (auth == None):
            abort(400, {'debug': 'Unsupported authorization type'})
            
        session_id = auth.group(1)
        session = db.session.query(Session).filter(Session.session_id == session_id).limit(1).first()
        
        if (session == None or session.is_expired()):
            abort(401, {'message': 'Please login again', 'debug': 'Session key expired or does not exist'})
            
        request.session = session
        request.user = session.user
        return func(*args, **kwargs)
    return wrapper

def requires_json(func):
    @wraps(func)
    def wrapper():
        body = request.json
        if (body == None):
            abort(400, {'debug': 'Request body missing'})
            
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
                debug = ''
                for key, type in invalid.items():
                    debug += '\'{0}\' was expected to be a {1}, '.format(key, type.__name__)
                abort(400, {'debug': debug})

            return func(**body)
        return wrapper
    return _validate_types
