from api.helpers import requires_json, requires_auth
from config import app, db
from datetime import datetime

from database.event import Event, EventPhase, EventSchema
from database.role import Role, Roles
from database.user import User
from database.registration import Registration, RegistrationSchema
from database.notification import Notification
from database.session import Session
from database.registration import Registration, RegistrationSchema

from api.helpers import *
from flask import jsonify, request
import logging
from sqlalchemy import or_
from sqlalchemy import update


@app.route('/event/published_list', methods=['GET'])
def get_all_published_event():
    events = db.session.query(Event).filter(Event.phase == EventPhase.APPROVED).all()
    if events:
        events_schema = EventSchema(many=True)
        #events = events.schema.dump(self)
        result = events_schema.dump(events)
        return jsonify(result=result,
                       success=True)
    else:
        return {'message': 'There is no published event.',
                'success': False}


@app.route('/event/unpublished_list/<path:org_id>', methods=['GET'])
@requires_auth
def get_all_unpublished_event(org_id):
    events = db.session.query(Event).filter(or_(Event.phase == EventPhase.INITIALIZED,
                                                Event.phase == EventPhase.ARCHIVED),
                                                Event.organization_id == org_id).all()
    user = request.user
    if user.roles.filter(Role.role == Roles.MEMBER):
      return {'message': 'You are not allowed to see unpublished event',
              'success': False}

    if events:
        events_schema = EventSchema(many=True)
        result = events_schema.dump(events)
        return jsonify(result=result,
                       success=True)
    else:
        return {'message': 'There is no unpublished event.',
                'success': False}


@app.route('/event/add/<path:org_id>', methods=['POST'])
@requires_auth
def create_event(org_id):
    sessionObj = request.session
    creator_id = sessionObj.user_id

    roleObj = db.session.query(Role).filter(Role.user_id == creator_id,
                                            Role.organization_id == org_id).first()
    if roleObj is None or not roleObj:
        return {'message': "You do not have any role in this organization",
                'success': False}

    if roleObj.role != Roles.ADMIN:
        return {'message': 'You need to be an ADMIN in this organization to create events',
                'success': False}

    userObj = sessionObj.user
    orgObj = roleObj.organization
    contact = orgObj.contact

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
        "phase": EventPhase.INITIALIZED
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
        "info": "EVENT created"
    }

    notify_chairman = Notification(**notification_data)
    db.session.add(notify_chairman)
    db.session.commit()
    event_schema = EventSchema()

    result = {'message': event_schema.dump(new_event),
              'success': True}
    return result


@app.route('/event/delete_event/<path:event_id>', methods=['DELETE'])
@requires_auth
def delete_event(event_id):
    # Verified the organization id existed or not
    event = Event.query.filter_by(event_id=event_id).first()
    if event is None or not event:
        return jsonify(success=False,
                       message="The event does not exists.")
    else:
        # Get the session token
        sessionObj = request.session
        # print("...SESSION TOKEN...")
        # print(sessionObj)
        user_role = db.session.query(Role).filter(Role.organization_id == event.organization_id,
                                                  Role.user_id == sessionObj.user_id).first()
        # Only chairman or admin can delete an event.
        if user_role.role == Roles.CHAIRMAN or user_role.role == Roles.ADMIN:
            # An event can be deleted only if it is not published.
            if event.phase == EventPhase.APPROVED:
                return jsonify(success=False,
                               message="The event is published so it cannot be deleted.")

            #notifications = Notification.query.filter_by(event_id=event_id).all()
            #db.session.delete(notifications)

            db.session.delete(event)
            db.session.commit()
            return jsonify(success=True,
                           message=event.event_name + " is deleted.")
        else:
            return jsonify(success=False,
                           message="You are not chairman or admin.")


@app.route('/event/register/<path:event_id>', methods=['POST'])
@requires_auth
def register_event(event_id):
    """ User register for a organization"""
    # Verified the organization id existed or not
    event_obj = Event.query.filter_by(event_id=event_id).first()
    if not event_obj or event_obj is None or event_obj.phase == EventPhase.INITIALIZED or event_obj.phase == EventPhase.ARCHIVED:
        return jsonify(success=False,
                       message="The event does not exists.")
    else:
        sessionObj = request.session
        #print("...SESSION TOKEN...")
        #print(sessionObj)
        register_id = sessionObj.user_id
        exist_register = Registration.query.filter_by(event_id=event_obj.event_id, register_id=register_id).first()
        if exist_register:
            return jsonify(success=False,
                           message="You already have been registered for this event.")
        else:
            new_registration = Registration(register_id=register_id,
                                            event_id=event_obj.event_id)
            db.session.add(new_registration)
            db.session.commit()
            return jsonify(success=True,
                           message="You registered for " + event_obj.event_name)


@app.route('/event/participants/<path:event_id>', methods=['GET'])
@requires_auth
def get_all_participants(event_id):
    registers = Registration.query.filter_by(event_id=event_id).all()
    if not registers or registers is None:
        return {'message': 'There is no participant.',
                'success': False}
    else:
        participants = []
        for register in registers:
            register_obj = db.session.query(User).filter(User.user_id == register.register_id).first()
            data = {
                'name': register_obj.name,
                'user_id': register.register_id
            }
            participants.append(data)
        return jsonify({'success': True, 'message': 'Show all participants', 'participants': participants})


@app.route('/event/unregister/<path:event_id>', methods=['DELETE'])
@requires_auth
def unregister_event(event_id):
    """ User register for a organization"""
    # Verified the organization id existed or not
    event_obj = Event.query.filter_by(event_id=event_id).first()
    event_name = event_obj.event_name
    sessionObj = request.session
    register_obj = db.session.query(Registration).filter(Registration.register_id == sessionObj.user_id,
                                                         Registration.event_id == event_id).first()

    if not register_obj or register_obj is None:
        return jsonify(success=False,
                       message="You haven't registered for this event.")
    else:
        db.session.delete(register_obj)
        db.session.commit()
        return jsonify(success=True,
                        message="You successfully unregister for " + event_name)


@app.route('/event/approve/<path:event_id>', methods=['PUT'])
@requires_auth
def approve_event(event_id):
    sessionObj = request.session
    creator_id = sessionObj.user_id
    eventObj = db.session.query(Event).filter(Event.event_id == event_id).first()

    roleObj = db.session.query(Role).filter(Role.user_id == creator_id,
                                            Role.organization_id == eventObj.organization_id).first()
    print("DEBUG...")
    print(eventObj)
    print(roleObj)
    if roleObj is None or not roleObj:
        return {'message': "You do not have any role in this organization",
                'success': False}

    if roleObj.role != Roles.CHAIRMAN:
        return {'message': 'You need to be an CHAIRMAN in this organization to approve events',
                'success': False}
    eventObj.phase = EventPhase.APPROVED
    db.session.commit()
    event_schema = EventSchema()

    result = {'message': event_schema.dump(eventObj),
              'success': True}

    return result

@app.route('/event/cancel/<path:event_id>', methods=['PUT'])
@requires_auth
def cancel_event(event_id):
    sessionObj = request.session
    creator_id = sessionObj.user_id
    eventObj = db.session.query(Event).filter(Event.event_id == event_id).first()
    if eventObj is None or not eventObj:
        return {'message': "This event does not exist !!! ",
                'success': False}

    roleObj = db.session.query(Role).filter(Role.user_id == creator_id,
                                            Role.organization_id == eventObj.organization_id).first()
    print("DEBUG...")
    print(eventObj)
    print(roleObj)
    # if the event exist, check a status of the person
    if roleObj is None or not roleObj:
        return {'message': "You do not have any role in this organization",
                'success': False}

    if roleObj.role != Roles.CHAIRMAN:
        return {'message': 'You need to be an CHAIRMAN in this organization to cancel events',
                'success': False}
    # This is admin or chairman
    eventObj.phase = EventPhase.ARCHIVED
    db.session.commit()
    event_schema = EventSchema()

    result = {'message': event_schema.dump(eventObj) + " have been canceled",
              'success': True}

    return result

@app.route('/event/<path:event_id>', methods=['POST'])
@requires_auth
@requires_json # TODO: Centralize validation on event fields input
def edit_event(event_id, **kwargs):
    user = request.user
    event = db.session.query(Event).filter(Event.event_id == event_id).first()
    role = user.roles.filter(
        Role.organization == event.organization,
        or_(Role.role == Roles.ADMIN, Role.role == Roles.CHAIRMAN)
    ).first()

    if role == None:
        return {'success': False, 'message': 'You don\'t have permission to do that!'}, 403
        
    # Perform post-processing/sanitization of fields
    kwargs['start_date'] = datetime.fromisoformat(kwargs['start_date'])
    kwargs['end_date'] = datetime.fromisoformat(kwargs['end_date'])
    
    # Only unpack certain fields to prevent other fields from being edited
    permitted_keys = ['event_name', 'start_date', 'end_date', 'theme', 'perks', 'categories', 'info']
    for key, value in kwargs.items():
        if key in permitted_keys: setattr(event, key, value)

    db.session.commit()
    return {'success': True, 'message': '', 'event': EventSchema().dump(event)}
