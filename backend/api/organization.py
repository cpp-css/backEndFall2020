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
def get_all_org():
    """
    Return all organizations
    ---
    tags:
        - organization
    response:
        200:
            description: OK
                content:
                    application/json:
                        schema:
                            type: object
                            properties:
                                success:
                                    type: boolean
                                result:
                                    type: array
                                    items:
                                        type: object
                                        properties:
                                            categories:
                                                type: string
                                            contact_id:
                                                type: string
                                            org_name:
                                                type: string
                                            organization:
                                                type: string
    """
    organizations = Organization.query.all()
    organizations_schema = OrganizationSchema(many=True)
    result = organizations_schema.dump(organizations)
    return jsonify(result=result,
                   success=True)


@app.route('/organization/<org_id>/events/published', methods=['GET'])
def get_all_published_events(org_id):
    """
    Show all published events of an events
    ---
        tags:
          - event
        response:
            200:
                description: OK
                content:
                    application/json:
                        schema:
                            type: object
                            properties:
                                success:
                                    type: boolean
                                result:
                                    type: array
                                    items:
                                        type: object
                                        properties:
                                            categories:
                                                type: string
                                            contact_id:
                                                type: string
                                            creator_id:
                                                type: string
                                            end_date:
                                                type: string
                                            event_id:
                                                type: string
                                            event_name:
                                                type: string
                                            info:
                                                type: string
                                            organization_id:
                                                type: string
                                            perks:
                                                type: string
                                            phase:
                                                type: integer
                                            start_date:
                                                type: string
                                            theme:
                                                type: string
    """
    # Verify the organize exists.
    organization = Organization.query.filter_by(organization_id=org_id).first()
    if organization is None:
        return jsonify(success=False,
                       message="The organization does not exists.")
    else:
        events = db.session.query(Event).filter((Event.organization_id == organization.organization_id),
                                                Event.phase == EventPhase.APPROVED).all()
        if events is None:
            return jsonify(success=False,
                           message="The organization does not have any events.")
        else:
            events_schema = EventSchema(many=True)
            result = events_schema.dump(events)
            return jsonify(result=result,
                           success=True)


@app.route('/organization/details/<path:org_id>', methods=['GET'])
def get_org_info(org_id):
    """
    Show an organization's details
    ---
    tags:
      - event
    response:
        200:
            description: OK
            content:
                application/json:
                    schema:
                        type: object
                        properties:
                            board:
                                type: array
                                item:
                                    type: object
                                    properties:
                                        name:
                                            type: string
                                        role:
                                            type: string
                                        user_id:
                                            type: string
                            categories:
                                type: string
                            org_name:
                                type: string
                            organization_id:
                                type: string
                            success:
                                type: boolean
    """
    # Verify the organize exists.
    organization = Organization.query.filter_by(organization_id=org_id).first()
    if not organization or organization is None:
        return jsonify(success=False,
                       message="The organization does not exists.")
    else:
        board = db.session.query(Role).filter(Role.organization_id == org_id,
                                              Role.role != Roles.MEMBER).all()
        board_members = []
        for member in board:
            user_obj = db.session.query(User).filter(User.user_id == member.user_id).first()
            print(user_obj.name, user_obj.email, member.role)
            data = {
                'name': user_obj.name,
                'user_id': user_obj.email,
                'role': member.role.name
            }
            board_members.append(data)
        return jsonify(success=True,
                       org_name=organization.org_name,
                       organization_id=organization.organization_id,
                       # admin_id=organization.admin_id,
                       board=board_members,
                       categories=organization.categories)


@app.route('/organization/show_members/<path:org_id>', methods=['GET'])
@requires_auth
def get_all_member(org_id):
    sessionObj = request.session
    # only user in an organization can see all members.
    is_in_org = db.session.query(Role).filter(Role.user_id == sessionObj.user_id).all()

    if is_in_org is None:
        return jsonify(message='You are not member of this organization', success=False)
    all_members = db.session.query(Role).filter(Role.organization_id == org_id, Role.role == Roles.MEMBER).all()

    if all_members is None or not all_members:
        return jsonify(message='This organization does not have any members', success=False)
    else:
        list_member = []
        for member in all_members:
            user_obj = db.session.query(User).filter(User.user_id == member.user_id).first()
            data = {
                'name': user_obj.name,
                'user_id': user_obj.email
            }
            list_member.append(data)
        return jsonify({'success': True, 'message': 'Show all members', 'members': list_member})


@app.route('/organization/add', methods=['POST'])
@requires_auth
def add_org():
    """
    Create a new organization
    ---
    tags:
        organization
    parameter:
        - in: body
            name: organization
            description: new organization
            require: true
            schema:
                type: object
                required:
                    - org_name
                    - categories
                    - contact
                properties:
                    org_name:
                        type: string
                    categories:
                        type: string
                    contact:
                        type: object
                        required:
                            - address
                            - state
                            - zipcode
                            - country
                            - dob
                        properties:
                            address:
                                type: string
                            state:
                                type: string
                            zipcode
                                type: integer
                            country:
                                type: string
                            dob:
                                type: string
                                description: An ISO 8601 formatted datetime string
    response:
        200:
            description: OK
            content:
                application/json:
                    schema:
                        type: object
                        properties:
                            success:
                                type: boolean
                            message:
                                type: string
    """
    sessionObj = request.session

    input_data = request.json
    org_name = input_data['org_name']
    categories = input_data['categories']
    contact_data = input_data['contact']
    exist_name = Organization.query.filter_by(org_name=org_name).first()

    if exist_name:
        return jsonify(message='This name is already taken. Please choose another name.', success=False)
    else:
        org_contact = Contact(**contact_data)

        new_org = Organization(org_name=org_name,
                               categories=categories,
                               contact=org_contact)

        chairman = Role(user_id=sessionObj.user_id,
                        organization=new_org,
                        role=Roles.CHAIRMAN)
        # organizations_schema = OrganizationSchema()
        db.session.add(new_org)
        db.session.add(chairman)
        db.session.commit()
        result = {'message': org_name + " is created",
                  'success': True}
        return jsonify(result)


@app.route('/organization/register/<path:org_id>', methods=['POST'])
@requires_auth
def register_org(org_id):
    """
    Register an organization.
    ---
    tags:
        - organization
    response:
        200:
            description: OK
            content:
                application/json:
                    schema:
                        type: object
                        properties:
                            success:
                                type: boolean
                            message:
                                type: string
    """
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
    """
    Unregister an organization or chairman resign
    ---
    tags:
        - organization
    parameter:
        - in: body
            name: email
            description: required if the user is Chairman
            required: false
            schema:
                required:
                    - email
                properties:
                    email:
                        type: string
    response:
        200:
            description: OK
            content:
                application/json:
                    schema:
                        type: object
                        properties:
                            success:
                                type: boolean
                            message:
                                type: string
    """
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
            if current_role.role == Roles.CHAIRMAN:
                # new_role_email = request.form.get('email')
                input_data = request.json
                new_role_email = input_data['email']
                new_role = User.query.filter_by(email=new_role_email).first()
                if new_role is None:
                    return jsonify(success=False,
                                   message="The email doesn't exist.")
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
                'end_date': managed.end_date,
                'phase': managed.phase.name
            }
            managed_orgs.append(data)
        return jsonify(
            {'success': True, 'organization': org_name, 'message': 'Show all events managed by this organization',
             'result': managed_orgs})
    else:
        return {'message': 'This organization has no registered events.',
                'success': False}
