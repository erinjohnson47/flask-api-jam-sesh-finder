import models

from flask import Blueprint, request, jsonify
from flask_login import login_user, current_user, login_required, logout_user
from playhouse.shortcuts import model_to_dict

event = Blueprint('events', 'event', url_prefix='/event')

@event.route('/', methods=["GET"])
def get_all_events():
    print('event get all route')
    try:
        events = [model_to_dict(event) for event in models.Event.select()]
        return jsonify(data=events, status={"code": 200, "message": "Success"})
    except models.DoesNotExist:
        return jsonify(data={}, status={"code": 401, "message": "Error getting the resources"})

@event.route('/', methods=["POST"])
def create_event():
    payload = request.get_json()
    print(payload, "payload")
    print(current_user, type(current_user), current_user.get_id(), 'this is current_user right before event creation')
    event = models.Event.create(**payload, created_by = current_user.get_id())
    event_dict = model_to_dict(event)
    print(event_dict, '<-event_dict in create event route in flask')
    return jsonify(data=event_dict, status={"code": 201, "message": "Success"})

@event.route('/<id>', methods=["PUT"])
def update_event(id):
    payload = request.get.json()
    print(payload)
    query = models.Event.update(**payload).where(models.Event.id==id)
    query.execute()
    return jsonify(data=model_to_dict(models.Event.get_by_id(id)), status={"code": 200, "message": "resource updated successfully"})

@event.route('/<id>', methods=["Delete"])
def delete_event(id):
    query = models.Event.delete().where(models.Event.id==id)
    query.execute()
    return jsonify(data='resource successfully deleted', status={"code": 200, "message": "resource deleted successfully"})

