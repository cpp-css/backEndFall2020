from config import app, db
from database.organization import Organization, OrganizationSchema
from database.session import Session
from flask import jsonify, request


@app.route('/organization/list', methods=['GET'])
def show_all_org():
    """ Return all organizations """
    organizations = Organization.query.all()
    organizations_schema = OrganizationSchema(many=True)
    result = organizations_schema.dump(organizations)
    return jsonify(result=result,
                   success=True)


@app.route('/organization/details/<path:org_id>', methods=['GET'])
def show_org(org_id):
    """ Return a specific organization by its ID """
    organization = Organization.query.filter_by(organization_id=org_id).first()
    if organization:
        return jsonify(success=True,
                       org_name=organization.org_name,
                       organization_id=organization.organization_id,
                       admin_id=organization.admin_id,
                       chairman_id=organization.chairman_id,
                       categories=organization.categories)
    else:
        return jsonify(success=False,
                       message="The organization does not exists")


@app.route('/organization/add', methods=['POST'])
def add_org():
    """ Add new organization """
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
        result = {'message': {'org_name': org_name, 'categories': categories, 'contact_id': contact_id}, 'success': True}
        db.session.add(new_org)
        db.session.commit()
    return jsonify(result)


@app.route('/organization/register', methods=['POST'])
def register_org():
    """ User register for a organization"""
    return jsonify(success=True,
                   message="Registered.")


@app.route('/organization/resign', methods=['POST'])
def resign_role():
    """ Resign admin/chairman """
    return jsonify(success=True,
                   message="Resigned.")
