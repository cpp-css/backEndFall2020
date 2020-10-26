from flask import json, jsonify
from traceback import format_tb
from werkzeug.exceptions import HTTPException

from config import DEBUG, app
from error.helpers import GENERIC_ERROR

@app.errorhandler(HTTPException)
def handle_http_exception(e):
    response = e.get_response()
    body = {'success': False, 'message': GENERIC_ERROR}

    # Ordered by level of specificity
    if DEBUG and 'debug' in e.description:
        # Exact cause of error specified
        body['message'] = '[DEBUG] {0}'.format(e.description['debug'])
    elif DEBUG:
        # Error caught by Flask
        body['message'] = '[DEBUG] {0}'.format(str(e))
        body['traceback'] = format_tb(e.__traceback__)
    elif 'message' in e.description:
        # Specific user displayable error
        body['message'] = e.description['message']

    response.data = json.dumps(body)
    response.content_type = "application/json"
    return response
