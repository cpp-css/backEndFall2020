
from config import app, db
from database.event import Event, EventSchema
from database.role import Role
from database.session import Session
from flask import jsonify, request


@app.route('/event/list', methods=['GET'])
def show_all_eve():
    events = Event.query.all()
    events_schema = EventSchema(many=True)
    result = events_schema.dump(events)
    return jsonify(result)

'''
@app.route('/event/add', methods=['POST'])
def add_eve():
    token = request.headers.get('Authorization')
    token = token.split()[1]
    #sessionObj = db.session.query(Session).filter(Session.session_id == token).first()
    roleObj = db.session.query(Role).filter(Role.role_id == token, Role.organization_id == request.form['organization_id']).first()
    #print("DEBUG....")
    #print(sessionObj)
    
    test_event = event.Event(creator=test_user,
                                   organization=test_org,
                                   start_date=datetime.now(tz=None),
                                   end_date=datetime.now(tz=None),
                                   theme=request.form['theme'],
                                   perks=request.form['perks'],
                                   categories=request.form['categories'],
                                   info=request.form['info'],
                                   phase=0,
                                   roleObj = db.session.query(Role).filter(Role.role_id == token, Role.organization_id == request.form['organization_id']).first())

    #eve_name = request.form['event_name']
    test = Event.query.filter_by(eve_name=eve_name).first()

    if test:
        return jsonify(message='This name is already taken. Please choose another name.', success=False)
    else:
        eve_name = request.form.get('eve_name')
        categories = request.form.get('categories')
        contact_id = request.form.get('contact_id')
        new_eve = Event(eve_name=eve_name,
                               categories=categories,
                               contact_id=contact_id,
                               chairman_id=sessionObj.user_id)
        result = {'message': {'eve_name': eve_name, 'categories': categories, 'contact_id': contact_id},
                  'success': True}

        db.session.add(new_eve)
        db.session.commit()
    return result

'''