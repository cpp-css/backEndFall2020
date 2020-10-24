from config import app, db
from database.event import Event, EventSchema
from flask import jsonify, request

@app.route('/event/paticipants/<path:org_id>', methods=['GET'])
def get_all_participants(org_id):
    """ Return list of all participants in a event by its ID """
    event = Event.query.filter_by(event_id=org_id).first()
    if event:
        event_schema = EventSchema()
        result = event_schema.dump(event)
        return jsonify(result)
    else:
        return jsonify(success=False,
                       message="The organization does not exists")