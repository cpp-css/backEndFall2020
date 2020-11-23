from flask import json, jsonify
from traceback import format_tb
import logging
from werkzeug.exceptions import HTTPException

from config import DEBUG, app
from error.helpers import GENERIC_ERROR

logger = logging.getLogger('error.http')

@app.errorhandler(HTTPException)
def handle_http_exception(e):
    response = e.get_response()
    body = {'success': False, 'message': GENERIC_ERROR}

    if 'debug' in e.description:
        debug_message = e.description['debug']
        logger.error(debug_message)
    else:
        debug_message = str(e)
        traceback = format_tb(e.__traceback__)
        logger.error('{0}\nTraceback:\n{1}'.format(debug_message, ''.join(traceback)))

    # Ordered by level of specificity
    if DEBUG and 'debug' in e.description:
        # Exact cause of error specified
        body['message'] = '[DEBUG] {0}'.format(debug_message)
    elif DEBUG:
        # Error caught by Flask
        body['message'] = '[DEBUG] {0}'.format(debug_message)
        body['traceback'] = traceback
    elif 'message' in e.description:
        # Specific user displayable error
        body['message'] = e.description['message']

    response.data = json.dumps(body)
    response.content_type = "application/json"
    return response
