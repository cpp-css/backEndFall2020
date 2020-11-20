from config import app, db

from api.helpers import *
from database.organization import Organization, OrganizationSchema
from database.contact import Contact
from database.user import User
from database.role import Role, Roles
from database.session import Session
from database.role import Role, RoleSchema
from database.user import User, UserSchema
from database.event import Event, EventSchema, EventPhase
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

@app.route('/organization/<org_id>/events/published', methods=['GET'])
def show_all_published_events(org_id):
    """ Return a specific organization by its ID """
    # Verify the organize exists.
    organization = Organization.query.filter_by(organization_id=org_id).first()
    if organization:
        events = db.session.query(Event).filter((Event.organization_id == organization.organization_id), Event.phase == EventPhase.APPROVED).all()
        events_schema = EventSchema(many=True)
        result = events_schema.dump(events)
        #result = EventSchema.dump(events, many=True)
        return jsonify(result=result,
                   success=True)
    else:
        return jsonify(success=False,
                       message="The organization does not exists.")

@app.route('/organization/details/<path:org_id>', methods=['GET'])
def show_org(org_id):
    """ Return a specific organization by its ID """
    # Verify the organize exists.
    organization = Organization.query.filter_by(organization_id=org_id).first()
    if not organization or organization is None:
        return jsonify(success=False,
                       message="The organization does not exists.")
    else:
        return jsonify(success=True,
                       org_name=organization.org_name,
                       organization_id=organization.organization_id,
                       # admin_id=organization.admin_id,
                       # chairman_id=organization.chairman_id,
                       categories=organization.categories)


@app.route('/organization/showMembers/<path:org_id>', methods=['GET'])
def get_all_member(org_id):
    all_members = db.session.query(Role).filter(Role.organization_id == org_id, Role.role == Roles.MEMBER).all()

    if all_members is None or not all_members:
        return jsonify(message='This organization does not exist', success=False)
    else:
        list_member = []
        for member in all_members:
            user_obj = db.session.query(User).filter(User.user_id == member.user_id).first()
            data = {
                'name': user_obj.name,
                'user_id': user_obj.email
            }
            list_member.append(data)
        return jsonify({'success': True, 'message': 'Show all members', 'participants': list_member})


@app.route('/organization/add', methods=['POST'])
@requires_auth
def add_org():
    sessionObj = request.session

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
@requires_auth
def register_org(org_id):
    """ User register for a organization"""
    organization = Organization.query.filter_by(organization_id=org_id).first()
    if organization is None:
        return jsonify(success=False,
                       message="The organization does not exists.")
    else:
        sessionObj = request.session

        current_role = Role.query.filter_by(organization_id=org_id, user_id=sessionObj.user_id).first()
        if current_role:  # Already in the organization
            return jsonify(success=False,
                           message="You already have been registered for this organization.")
        else:
            new_member = Role(user_id=sessionObj.user_id,
                              organization=organization,
                              role=Roles.MEMBER)
            db.session.add(new_member)
            db.session.commit()
            return jsonify(success=True,
                           message="You registered for " + organization.org_name)


@app.route('/organization/resign/<path:org_id>', methods=['DELETE'])
@requires_auth
def unregister_org(org_id):
    """ Resign admin/chairman """
    # Verified the organization id existed or not
    organization = Organization.query.filter_by(organization_id=org_id).first()
    if organization is None:
        return jsonify(success=False,
                       message="The organization does not exists.")
    else:
        # Get the session token
        sessionObj = request.session

        # Query the the role matches the organization and the user.
        current_role = Role.query.filter_by(organization_id=org_id, user_id=sessionObj.user_id).first()
        if current_role is None:
            return jsonify(success=False,
                           message="You are not member of this organization.")
        else:
            # Check if the user is chairman or admin.
            if current_role.role == Roles.CHAIRMAN:
                # Resign chairman by enter new chairman's email.
                new_role_email = request.form.get('email')
                new_role = User.query.filter_by(email=new_role_email).first()
                # Assign new chairman to the organization.
                current_role.user = new_role

                db.session.commit()
                old_role = User.query.filter_by(user_id=sessionObj.user_id).first()  # get the old admin or chairman
                role = str(current_role.role).split(".")[1]  # get the role for print out
                return jsonify(success=True,
                               message=old_role.name + " resigned. " + new_role.name + " becomes " + role + " of " + organization.org_name)
            else:  # ADMIN OR TEAM MEMBERS
                db.session.delete(current_role)
                db.session.commit()
                return jsonify(success=True,
                               message="We will miss you.")

@app.route('/organization/managed_events/<path:organization_id>', methods=['GET'])
def get_managed_events(organization_id):
    managed_events = Event.query.filter_by(organization_id=organization_id).all()
    org_obj = Organization.query.filter_by(organization_id=organization_id).first()
    org_name = org_obj.org_name
    managed_orgs = []
    if managed_events:
        for managed in managed_events:
            data = {
                'event_id': managed.event_id,
                'event_name': managed.event_name,
                'start_date': managed.start_date,
                'end_date': managed.end_date
            }
            managed_orgs.append(data)
        return jsonify({'success': True, 'organization': org_name, 'message': 'Show all events managed by this organization',
                        'result': managed_orgs})
    else:
        return {'message': 'This organization has no registered events.',
                'success': False}

