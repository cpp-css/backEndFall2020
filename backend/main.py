import os
from config import app
from database.organization import Organization, OrganizationSchema
from flask import jsonify


@app.route('/')
def hello_world():
    return 'Hello, World!'


@app.route('/organizations', methods=['GET'])
def organization():
    organizations = Organization.query.all()
    organizations_schema = OrganizationSchema(many=True)
    result = organizations_schema.dump(organizations)
    return jsonify(result)


if __name__ == "__main__":
    port = os.getenv("PORT", 9090)
    app.run(host="localhost", port=port, threaded=True, debug=True)
