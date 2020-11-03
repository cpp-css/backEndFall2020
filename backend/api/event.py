from config import app, db
from datetime import datetime
from database.event import Event, EventSchema
from database.role import Role, Roles
from database.notification import Notification
from database.session import Session
from flask import jsonify, request
from sqlalchemy import or_


@app.route('/event/published_list', methods=['GET'])
def show_all_published_event():
    events = Event.query.filter(Event.phase == 1)
    events_schema = EventSchema(many=True)
    result = events_schema.dump(events)
    return jsonify(result)


@app.route('/event/unpublished_list', methods=['GET'])
def show_all_unpublished_event():
    events = Event.query.filter(or_(Event.phase == 0, Event.phase == 2))
    events_schema = EventSchema(many=True)
    result = events_schema.dump(events)
    return jsonify(result)


@app.route('/event/add/<path:org_id>', methods=['POST'])
def add_event(org_id):
    token = request.headers.get('Authorization')
    token = token.split()[1]
    sessionObj = db.session.query(Session).filter(Session.session_id == token).first()
    creator_id = sessionObj.user_id

    roleObj = db.session.query(Role).filter(Role.user_id == creator_id,
                                            Role.organization_id == org_id).first()
    userObj = sessionObj.user
    orgObj = roleObj.organization
    contact = orgObj.contact

    if roleObj.role != Roles.ADMIN:
        return {'message': 'You need to be an ADMIN in this organization to create events',
                'success': False }

    input_data = request.json

    event_data = {
        "creator": userObj,
        "organization": orgObj,
        "contact": contact,
        "event_name": input_data['event_name'],
        "start_date": datetime.fromisoformat(input_data['start_date']),
        "end_date": datetime.fromisoformat(input_data['end_date']),
        "theme": input_data['theme'],
        "perks": input_data['perks'],
        "categories": input_data['categories'],
        "info": input_data['info'],
        "phase": 0
    }
    #print("DEBUG....")
    #print(sessionObj)
    is_event_name_exist = Event.query.filter_by(event_name=event_data['event_name']).first()
    if is_event_name_exist:
        return jsonify(message='This name is already taken. Please choose another name.', success=False)

    new_event = Event(**event_data)
    db.session.add(new_event)

    chairmanObj = db.session.query(Role).filter(Role.role == Roles.CHAIRMAN,
                                                Role.organization_id == org_id).first()

    notification_data = {
        "sender": userObj,
        "receiver": chairmanObj.user,
        "event": new_event,
        "info": "A new event has been created"
    }

    notify_chairman = Notification(**notification_data)
    db.session.add(notify_chairman)
    db.session.commit()
    event_schema = EventSchema()

    result = {'message': event_schema.dump(new_event),
              'success': True}
    return result
