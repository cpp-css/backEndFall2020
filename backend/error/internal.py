from flask import jsonify
from traceback import format_tb
import logging
from werkzeug.exceptions import HTTPException

from config import DEBUG, app
from error.helpers import GENERIC_ERROR

logger = logging.getLogger('error.internal')

@app.errorhandler(Exception)
def handle_exception(e):
    if isinstance(e, HTTPException):
        return e
    
    debug_message = str(e)
    traceback = format_tb(e.__traceback__)
    logger.error('{0}\nTraceback:\n{1}'.format(debug_message, ''.join(traceback)))
    
    response = {'success': False, 'message': GENERIC_ERROR}
    
    if DEBUG:
        response['message'] = '[DEBUG] {0}'.format(debug_message)
        response['traceback'] = traceback

    return jsonify(response), 500
