
from config import app, db
from database.role import Role, RoleSchema
from database.session import Session
from flask import jsonify, request


@app.route('/admins/list', methods=['GET'])
def show_all_admins():
    """ Search in role, if role  = 1 is admins, else skip. Print all admins out"""
    admins = Role.query.all()
    role_schema = RoleSchema(many=True)
    result = role_schema.dump(admins)
    return jsonify(result)


@app.route('/admins/add', methods=['POST'])
def make_admin():
    token = request.headers.get('Authorization')
    token = token.split()[1]
    sessionObj = db.session.query(Session).filter(Session.session_id == token).first()
    print("DEBUG....")
    print(sessionObj)

    contact_id = request.form['user_id']
    test = Organization.query.filter_by(contact_id=contact_id).first()

    if test:
        # Name is already existed -> admin is added or not?
        # test2 = Organization.query.filter_by(admin_id=contact_id).first()
        return jsonify(message='This name is already taken. Please choose another name.', success=False)
    else:
        org_name = request.form.get('org_name')
        categories = request.form.get('categories')
        contact_id = request.form.get('contact_id')
        admin_id = request.form.get('admin_id')
        new_org = Organization(org_name=org_name,
                               categories=categories,
                               contact_id=contact_id, admin_id= admin_id,
                               chairman_id=sessionObj.user_id)
        result = {'message': {'org_name': org_name, 'categories': categories, 'contact_id': contact_id},
                  'success': True}

        db.session.add(new_org)
        db.session.commit()
    return result

