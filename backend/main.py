import os
from config import app, db
import api.organization
import api.user
import api.event
import error.http
import error.internal


@app.route('/')
def hello_world():
    return 'Hello, World!'


if __name__ == "__main__":
    port = os.getenv("PORT", 9090)
    app.run(host="localhost", port=port, threaded=True, debug=True)
