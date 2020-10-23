from flask import jsonify
from traceback import format_tb
from werkzeug.exceptions import HTTPException

from config import DEBUG, app
from error.helpers import GENERIC_ERROR

# TODO: log unhandled app exceptions to central location

@app.errorhandler(Exception)
def handle_exception(e):
    if isinstance(e, HTTPException):
        return e
        
    response = {'success': False, 'message': GENERIC_ERROR}
    
    if DEBUG:
        response['message'] = '[DEBUG] {0}'.format(str(e))
        response['traceback'] = format_tb(e.__traceback__)

    return jsonify(response), 500
