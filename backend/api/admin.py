
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

    organization_id = request.form['organization_id']
    print("DEBUG....line 31")
    print(creator_id)
    print(organization_id)
    # check the creator_id is the person created this organization id
    roleObject = db.session.query(Role).filter(Role.user_id == creator_id,
                                               Role.organization_id == organization_id).first()
    print("DEBUG.... line 33")
    print(roleObject)

    if roleObject.role != Roles.CHAIRMAN:  # this is not a chairnman
        return jsonify(message='You do not allow to make admin', success=False)
    else:  # this is a chairman
        email = request.form['email']
        user_object = User.query.filter_by(email=email).first()  # dictionary
        # check if this person has user id in organization
        newAdminRole = db.session.query(Role).filter(Role.user_id == user_object.user_id,
                                                     Role.organization_id == organization_id).first()
        print("DEBUG.... line 42")
        print(newAdminRole)
        # the person not in the organization -> add this user into organization and set rule is admin
        if not newAdminRole:
            user_id_input = user_object.user_id
            organization_id_input = organization_id
            role_input = Roles.ADMIN
            new_admin = Role(user_id=user_id_input,
                             organization_id=organization_id_input,
                             role=role_input)
            result = {'message': {'User_id': user_id_input, 'organization': organization_id_input, 'role': role_input},
                      'success': True}
            print("New user have been added and set to be admin")
            db.session.add(new_admin)
            db.session.commit()
            return jsonify(result)
        else:
            # this user is in the organization
            if newAdminRole.role == Roles.ADMIN:
                return jsonify(message='This user is already admin of the organization', success=False)
            else:
                newAdminRole.role = Roles.ADMIN
                print(newAdminRole.role)
                return jsonify(message='Change the role of this member to be admin', success=False)


@app.route('/admins/remove_admin1', methods=['POST'])
def remove_admin():
    token = request.headers.get('Authorization')
    token = token.split()[1]
    sessionObj = db.session.query(Session).filter(Session.session_id == token).first()
    creator_id = sessionObj.user_id
    print("DEBUG....")
    print(sessionObj)

    organization_id = request.form['organization_id']
    print("DEBUG....line 31")
    print(creator_id)
    print(organization_id)
    # check the creator_id is the person created this organization id
    roleObject = db.session.query(Role).filter(Role.user_id == creator_id,
                                               Role.organization_id == organization_id).first()
    print("DEBUG.... line 33")
    print(roleObject)

    if roleObject.role != Roles.CHAIRMAN:  # this is not a chairnman
        return jsonify(message='You do not allow to remove admin', success=False)
    else:  # this is a chairman
        email = request.form['email']
        user_object = User.query.filter_by(email=email).first()  # dictionary
        #check if this person has user id in organization
        newAdminRole = db.session.query(Role).filter(Role.user_id == user_object.user_id,
                                                     Role.organization_id == organization_id).first()
        print("DEBUG.... line 42")
        print(newAdminRole)
        # the person not in the organization -> return error
        if not newAdminRole:
            return jsonify(message='This user is not in the organization', success=False)
        else:
            #this user is in the organization
            if newAdminRole.role == Roles.ADMIN:
                newAdminRole.role = Roles.MEMBER
                db.session.commit()
                return jsonify(message='This user is admin of the organization. Remove role completely -> this user role change to member', success=True)
            else:
                return jsonify(message='This user is not ADMIN. Cannot remove Admin !!!', success=False)
