from config import app, db
from database.organization import Organization, OrganizationSchema
from database.contact import Contact
from database.user import User
from database.role import Role, Roles
from database.session import Session
from database.role import Role, RoleSchema
from database.user import User, UserSchema
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
    # Verify the organize exists.
    organization = Organization.query.filter_by(organization_id=org_id).first()
    if organization:
        return jsonify(success=True,
                       org_name=organization.org_name,
                       organization_id=organization.organization_id,
                       #admin_id=organization.admin_id,
                       #chairman_id=organization.chairman_id,
                       categories=organization.categories)
    else:
        return jsonify(success=False,
                       message="The organization does not exists.")


@app.route('/organization/showMembers', methods=['GET'])
def show_all_member():
    token = request.headers.get('Authorization')
    token = token.split()[1]
    sessionObj = db.session.query(Session).filter(Session.session_id == token).first()
    print("DEBUG....")
    print(sessionObj)

    org_name = request.form['org_name']
    test = Organization.query.filter_by(org_name=org_name).first()
    print("DEBUG....")
    print(test)
    #this name exist -> print all member
    if test:
        # print all member
        member = Role.query.all()
        member_schema = RoleSchema(many=True)
        result = member_schema.dump(member)
        return jsonify(result)
    else:  # this is not exist
        return jsonify(message='This organization does not exist', success=False)


@app.route('/organization/add', methods=['POST'])
def add_org():
    """ Add new organization """
    # Get the session by verify the token and get the user_id
    token = request.headers.get('Authorization')
    token = token.split()[1]
    sessionObj = db.session.query(Session).filter(Session.session_id == token).first()
    #print("DEBUG....")
    #print(sessionObj)

    # Test if the organization exists.
    input_data = request.json
    org_name = input_data['org_name']
    categories = input_data['categories']
    contact_data = input_data['contact']
    exist_name = Organization.query.filter_by(org_name=org_name).first()

    if exist_name:
        return jsonify(message='This name is already taken. Please choose another name.', success=False)
    else:
        # New contact for the organization
        org_contact = Contact(**contact_data)

        # Create new organization
        new_org = Organization(org_name=org_name,
                               categories=categories,
                               contact=org_contact)

        # Create chairman for the organization
        chairman = Role(user_id=sessionObj.user_id,
                        organization=new_org,
                        role=Roles.CHAIRMAN)
        organizations_schema = OrganizationSchema()
        db.session.add(new_org)
        db.session.add(chairman)
        db.session.commit()
        result = {'message': organizations_schema.dump(new_org),
                  'success': True}
        return jsonify(result)


@app.route('/organization/register/<path:org_id>', methods=['POST'])
def register_org(org_id):
    """ User register for a organization"""
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
        # If the user is not in the organization, create new MEMBER role for the user.
        if current_role is None:
            new_member = Role(user_id=sessionObj.user_id,
                              organization=organization,
                              role=Roles.MEMBER)
            db.session.add(new_member)
            db.session.commit()
            return jsonify(success=True,
                           message="You registered for " + organization.org_name)
        else:
            return jsonify(success=False,
                           message="You already have been registered for this organization.")
    else:
        return jsonify(success=False,
                       message="The organization does not exists.")


@app.route('/organization/resign/<path:org_id>', methods=['DELETE'])
def unregister_org(org_id):
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
            if current_role.role == Roles.CHAIRMAN:
                # Resign chairman or admin role by enter new chairman or admin's email.
                new_role_email = request.form.get('email')
                new_role = User.query.filter_by(email=new_role_email).first()
                # Assign new chairman to the organization.
                current_role.user = new_role

                db.session.commit()
                old_role = User.query.filter_by(user_id=sessionObj.user_id).first()  # get the old admin or chairman
                role = str(current_role.role).split(".")[1]  # get the role for print out
                return jsonify(success=True,
                               message=old_role.name + " resigned. " + new_role.name + " becomes " + role + " of " + organization.org_name)
            else: # ADMIN OR TEAM MEMBERS
                db.session.delete(current_role)
                db.session.commit()
                return jsonify(success=True,
                               message="We will miss you.")
        else:
            return jsonify(success=False,
                           message="You are not member of this organization.")
    else:
        return jsonify(success=False,
                       message="The organization does not exists.")
