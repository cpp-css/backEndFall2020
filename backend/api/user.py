from datetime import datetime, timedelta
from flask import jsonify, request
from sqlalchemy.exc import IntegrityError
from api.helpers import GENERIC_ERROR, requires_json, validate_types
from config import app, db, DEBUG
from database.user import User
from database.session import Session

@app.route('/login', methods=['POST'])
@requires_json
@validate_types(expected={'email': str, 'password': str})
def login(email, password):
    user = db.session.query(User).filter(User.email == email).limit(1).first()
    if (user == None or not user.verify_password(password)):
        return jsonify({'success': False, 'message': 'Invalid login details'})
    
    session = Session(user_id=user.user_id, expires=datetime.now() + timedelta(days=1))
    db.session.add(session)
    db.session.commit()
    
    return jsonify({
        'success': True,
        'message': '',
        'session': session.session_id,
        'expires': session.expires
    })

@app.route('/signup', methods=['POST'])
@requires_json
@validate_types(expected={'name': str, 'email': str, 'password': str})
def signup(name, email, password):
    try:
        user = User(email=email, name=name, password=password)
        db.session.add(user)
        db.session.commit()
    except (IntegrityError) as ex:
        return jsonify({'success': False, 'message': 'Email already registered'})
    
    session = Session(user_id=user.user_id, expires=datetime.now() + timedelta(days=1))
    db.session.add(session)
    db.session.commit()
    
    return jsonify({
        'success': True,
        'message': '',
        'session': session.session_id,
        'expires': session.expires
    })