from config import db, ma, app
from database import organization
from flask import jsonify


@app.route('/organizations', methods=['GET'])
def organization():
    organizations = organization.Organization.query.all()
    organization_schema = organization.OrganizationSchema(many=True)
    data = organization_schema.dump(organizations)
    return data
