from config import app, db
from datetime import datetime
from database.event import Event, EventSchema
from database.role import Role, Roles
from database.notification import Notification
from database.session import Session
from database.registration import Registration, RegistrationSchema
from flask import jsonify, request
from sqlalchemy import or_


@app.route('/event/published_list', methods=['GET'])
def show_all_published_event():
    events = db.session.query(Event).filter(Event.phase == 1).all()
    if events:
        events_schema = EventSchema(many=True)
        result = events_schema.dump(events)
        return jsonify(result=result,
                       success=True)
    else:
        return {'message': 'There is no published event.',
                'success': False}


@app.route('/event/unpublished_list', methods=['GET'])
def show_all_unpublished_event():
    events = db.session.query(Event).filter(or_(Event.phase == 0, Event.phase == 2)).all()
    if events:
        events_schema = EventSchema(many=True)
        result = events_schema.dump(events)
        return jsonify(result=result,
                       success=True)
    else:
        return {'message': 'There is no unpublished event.',
                'success': False}


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
                'success': False}

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
    # print("DEBUG....")
    # print(sessionObj)
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


@app.route('/event/delete_event/<path:event_id>', methods=['DELETE'])
def delete_event(event_id):
    # Verified the organization id existed or not
    event = Event.query.filter_by(event_id=event_id).first()
    if event:
        # Get the session token
        token = request.headers.get('Authorization')
        token = token.split()[1]
        sessionObj = db.session.query(Session).filter(Session.session_id == token).first()
        # print("...SESSION TOKEN...")
        # print(sessionObj)
        role = db.session.query(Role).filter(Role.organization_id == event.organization_id,
                                             Role.user_id == sessionObj.user_id).first()

        # Only chairman or admin can delete an event.
        if role.role == Roles.CHAIRMAN or role.role == Roles.ADMIN:
            # An event can be deleted only if it is not published.
            if event.phase == 1:
                return jsonify(success=False,
                               message="The event is published so it cannot be deleted.")
            event_name = event.event_name
            db.session.delete(event)
            db.session.commit()
            return jsonify(success=True,
                           message=event_name + " is deleted.")
        else:
            return jsonify(success=False,
                           message="You are not chairman or admin.")
    else:
        return jsonify(success=False,
                       message="The event does not exists.")


@app.route('/event/participants/<path:event_id>', methods=['GET'])
def get_all_participants(event_id):
    participants = Registration.query.filter_by(event_id=event_id).all()
    if participants:
        participants_schema = RegistrationSchema(many=True)
        result = participants_schema.dump(participants)
        return jsonify(success=True,
                       result=result)
    else:
        return {'message': 'There is no participant.',
                'success': False}
