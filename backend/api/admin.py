from config import app, db
from database.organization import Organization
from database.role import Role, Roles
from database.user import User, UserSchema
from database.session import Session
from flask import jsonify, request
from sqlalchemy import or_


@app.route('/organization/organizer/<path:org_id>', methods=['GET'])
def show_board(org_id):
    """ Search in role, if role  = 1 is admins, else skip. Print all admins out"""
    all_roles = Role.query.filter(Role.organization_id == org_id,
                                     or_(Role.role == Roles.ADMIN, Role.role == Roles.CHAIRMAN)).all()
    result = []
    for eachRole in all_roles:
        user_name = User.query.filter(User.user_id == eachRole.user_id).first()
        data = {
            'name': user_name.name,
            'role': str(eachRole.role).split(".")[1]
        }
        result.append(data)
        print("DEBUG", result)
    return jsonify({"success": True, "board": result})


@app.route('/organization/make_admin/<path:org_id>', methods=['POST'])
def make_admin(org_id):
    token = request.headers.get('Authorization')
    token = token.split()[1]
    sessionObj = db.session.query(Session).filter(Session.session_id == token).first()
    current_role = Role.query.filter_by(organization_id=org_id, user_id=sessionObj.user_id).first()
    print("DEBUG....")
    print(current_role)
    if not current_role:
        return jsonify(message='You do not allow to do anything', success=False)
    else:
        # Check if the user is chairman or admin.
        if current_role.role == Roles.CHAIRMAN:
            input_data = request.json
            new_role_email = input_data['email']
            new_user = User.query.filter_by(email=new_role_email).first()
            # check if the new_user is already in board
            board_role = Role.query.filter(Role.user_id == new_user.user_id,
                                           Role.organization_id == org_id,
                                           Role.role != Roles.MEMBER).first()
            # 1 ADMIN -> board_role not None
            # 2 CHAIRMAN -> board_role not None
            # MEMBER or out side -> can able to make admin
            if board_role:
                return jsonify(message='New user is already on board', success=False)

            new_admin = Role(user_id=new_user.user_id,
                             organization_id=org_id,
                             role=Roles.ADMIN)
            result = {'message': new_user.name + " is our new Admin",
                      'success': True}
            db.session.add(new_admin)
            db.session.commit()
            return jsonify(result)
        else:
            return jsonify(message='You do not allow to make admin', success=False)


@app.route('/admins/remove_admin/<path:org_id>', methods=['POST'])
def remove_admin(org_id):
    token = request.headers.get('Authorization')
    token = token.split()[1]
    sessionObj = db.session.query(Session).filter(Session.session_id == token).first()
    current_role = Role.query.filter_by(organization_id=org_id, user_id=sessionObj.user_id).first()
    print("DEBUG....")
    print(current_role)
    if not current_role:
        return jsonify(message='You do not allow to do anything', success=False)
    else:
        # Check if the user is chairman or admin.
        if current_role.role == Roles.CHAIRMAN:
            input_data = request.json
            old_role_email = input_data['email']
            old_user = User.query.filter_by(email=old_role_email).first()
            old_admin = Role(user_id=old_user.user_id,
                             organization_id=org_id,
                             role=Roles.ADMIN)

            db.session.remove(old_admin)
            db.session.commit()
            result = {'message': old_user.name + " removed from admin",
                      'success': True}
            return jsonify(result)
        else:
            return jsonify(message='You do not allow to make admin', success=False)


