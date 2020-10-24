from config import app, db
from database.organization import Organization, OrganizationSchema
from database.session import Session
from flask import jsonify, request


@app.route('/organization/list', methods=['GET'])
def show_all_org():
    organizations = Organization.query.all()
    organizations_schema = OrganizationSchema(many=True)
    result = organizations_schema.dump(organizations)
    return jsonify(result)


@app.route('/organization/details/<path:org_name>', methods=['GET'])
def show_org(org_name):
    organization = Organization.query.filter_by(org_name=org_name).first()
    if organization:
        organization_schema = OrganizationSchema()
        result = organization_schema.dump(organization)
        return jsonify(result)
    else:
        return jsonify(success=False,
                       message="The organization does not exists")


@app.route('/organization/add', methods=['POST'])
def add_org():
    token = request.headers.get('Authorization')
    token = token.split()[1]
    sessionObj = db.session.query(Session).filter(Session.session_id == token).first()
    print("DEBUG....")
    print(sessionObj)

    org_name = request.form['org_name']
    test = Organization.query.filter_by(org_name=org_name).first()

    if test:
        return jsonify(message='This name is already taken. Please choose another name.', success=False)
    else:
        org_name = request.form.get('org_name')
        categories = request.form.get('categories')
        contact_id = request.form.get('contact_id')
        new_org = Organization(org_name=org_name,
                               categories=categories,
                               contact_id=contact_id,
                               chairman_id=sessionObj.user_id)
        result = {'message': {'org_name': org_name, 'categories': categories, 'contact_id': contact_id},
                  'success': True}

        db.session.add(new_org)
        db.session.commit()
    return result
