
from config import app, db
from database.organization import Organization
from database.role import Role, Roles
from database.user import User, UserSchema
from database.session import Session
from flask import jsonify, request


@app.route('/admins/list', methods=['GET'])
def show_all_admins():
    """ Search in role, if role  = 1 is admins, else skip. Print all admins out"""
    admins = Role.query.all()
    role_schema = RoleSchema()
    result = role_schema.dump(admins)
    return jsonify(result)


@app.route('/admins/make_admin', methods=['POST'])
def make_admin():
    token = request.headers.get('Authorization')
    token = token.split()[1]
    sessionObj = db.session.query(Session).filter(Session.session_id == token).first()
    creator_id = sessionObj.user_id
    print("DEBUG....")
    print(sessionObj)
    email = request.form['email']
    user_object = User.query.filter_by(email=email).first() # dictionary
    print("DEBUG....line 29")
    print(creator_id)
    organization_id = request.form['organization_id']

    roleObject = db.session.query(Role).filter(Role.user_id == creator_id,
                                               Role.organization_id == organization_id).first()
    print("DEBUG.... line 33")
    print(roleObject)

    if roleObject.role != Role.CHAIRMAN: # this is not a chairnman
        return jsonify(message='You do not allow to make admin', success=False)
    else: # this is a chairman
        newAdminRole= db.session.query(Role).filter(Role.user_id == user_object.user_id,
                                                    Role.organization_id == organization_id).first()
        if newAdminRole.role == Role.ADMIN:
            return jsonify(message='This user is already admin of the organization', success=False)
        user_id_input = user_object.user_id
        organization_id_input = organization_id
        role_input = Role.ADMIN
        new_admin = Role(user_id=user_id_input,
                               organization_id=organization_id_input,
                               role=role_input)
        result = {'message': {'User_id': user_id_input, 'organization': organization_id_input, 'role': role_input},
                  'success': True}

        db.session.add(new_admin)
        db.session.commit()
    return result

"""
@app.route('/admins/remove_admin', methods=['POST'])
def remove_admin():
    token = request.headers.get('Authorization')
    token = token.split()[1]
    sessionObj = db.session.query(Session).filter(Session.session_id == token).first()
    print("DEBUG....")
    print(sessionObj)

    contact_id = request.form['user_id']
    test = Organization.query.filter_by(contact_id=contact_id).first()

    if test:
        # Name is already existed -> Is the name admin or not?
        test2 = Role.query.filter_by(admin_id=contact_id).first()
        # if Contact_id = 1, this contact is already admin -> set it to be members?. Else, nothing to do
        if test2:
            # Remove this an admin
            Role(contact_id) = Role.schema()
            result = role_schema.dump(test2)
            return jsonify(message='This name is already admin', success=False)
        else:
            return jsonify(message='This name is not the admin', success=False)

    else:  # Name does not exist, create a new name and set that name to be an admin of an existed organization
        return jsonify(message='This name does not exist in the organization', success=False)
    return result
"""
