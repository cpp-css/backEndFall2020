from config import app, db
from database.organization import Organization, OrganizationSchema
from database.contact import Contact
from database.user import User
from database.role import Role, Roles
from database.session import Session
from flask import jsonify, request
from datetime import datetime


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
                       message="The organization does not exists.")


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
        created_date = datetime.utcnow()

        # Create new contact for the organization
        org_contact = Contact(dob=created_date,
                              address="3801 W Temple Ave, Pomona,",
                              state="California",
                              zipcode=91768,
                              country="USA")

        # Create new organization
        new_org = Organization(org_name=org_name,
                               categories=categories,
                               contact=org_contact)

        # Create chairman for the organization
        chairman = Role(user_id=sessionObj.user_id,
                        organization=new_org,
                        role=Roles.CHAIRMAN)

        result = {'message': {'org_name': org_name, 'categories': categories},
                  'success': True}
        db.session.add(new_org)
        db.session.add(chairman)
        db.session.commit()
    return jsonify(result)


@app.route('/organization/register', methods=['POST'])
def register_org():
    """ User register for a organization"""
    return jsonify(success=True,
                   message="Registered.")


@app.route('/organization/resign/<path:org_id>', methods=['PUT'])
def resign_role(org_id):
    """ Resign admin/chairman """
    # Verified the organization id existed or not
    organization = Organization.query.filter_by(organization_id=org_id).first()
    if organization:
        # Get the session token
        token = request.headers.get('Authorization')
        token = token.split()[1]
        sessionObj = db.session.query(Session).filter(Session.session_id == token).first()
        print("...SESSION TOKEN...")
        print(sessionObj)

        # Query the the role matches the organization and the user.
        current_role = Role.query.filter_by(organization_id=org_id, user_id=sessionObj.user_id).first()
        if current_role:
            # Check if the user is chairman or admin.
            if current_role.role == Roles.CHAIRMAN or current_role.role == Roles.ADMIN:
                # Resign chairman or admin role by enter new chairman or admin's email.
                new_role_email = request.form.get('email')
                new_role = User.query.filter_by(email=new_role_email).first()
                # Assign new chairman or admin to the organization.
                current_role.user = new_role

                db.session.commit()

                return jsonify(success=True,
                               message="Resigned.")
            else:
                return jsonify(success=False,
                               message="Cannot resign.")
        else:
            return jsonify(success=True,
                           message="You don't have any role in this organization.")
    else:
        return jsonify(success=False,
                       message="The organization does not exists.")
