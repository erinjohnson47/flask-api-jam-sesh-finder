import models


import os
import sys
import secrets
# from PIL import Image

from flask import Blueprint, request, jsonify, url_for, send_file

from flask_bcrypt import generate_password_hash, check_password_hash
from flask_login import login_user, current_user, login_required, logout_user
from playhouse.shortcuts import model_to_dict


user = Blueprint('users', 'user', url_prefix='/user')


@user.route('/register', methods=["POST"])
def register():
    print(request.files, request.form) 
    print(type(request))
    # pay_file = request.files ----stuff for image
    payload = request.form.to_dict()
    # dict_file = pay_file.to_dict()
    # print(type(payload), 'payload', type(payload), 'type')
    


    print(payload)
    # print(dict_file)

    payload['email'].lower()
    try:
        models.User.get(models.User.email == payload['email'])
        return jsonify(data={}, status={"code": 401, "message": "A user with that name or email exists"})
    except models.DoesNotExist: 
        payload['password'] = generate_password_hash(payload['password'])
        # file_picture_path = save_picture(dict_file['file'])
        # payload['image'] = file_picture_path

        user = models.User.create(**payload)
        print(type(user))
        login_user(user)

        # current_user.image = file_picture_path

        user_dict = model_to_dict(user)
        print(user_dict)
        print(type(user_dict))


        del user_dict['password']

        return jsonify(data=user_dict, status={"code": 201, "message": "Success"})



@user.route('/login', methods=["POST"])
def login():
    payload = request.form.to_dict()
    print(payload, '<-payload')
    try:
        user = models.User.get(models.User.username == payload['username'])
        user_dict = model_to_dict(user)
        if(check_password_hash(user_dict['password'], payload['password'])):
            del user_dict['password']
            login_user(user)
            print(current_user, '<-current user')
            print(user_dict, '<-user_dict')
            return jsonify(data=user_dict, status={"code": 200, "message": "Success"})
        else:
            return jsonify(data={}, status={"code": 401, "message": "Username or Password is incorrect"})
    except models.DoesNotExist:
        return jsonify(data={}, status={"code": 401, "message": "Username or Password is incorrect"})

@user.route('/logout', methods=["GET"])
@login_required
def logout():
    logout_user()
    return "logged out"


@user.route('/<id>', methods=["PUT"])
@login_required
def update(id):
    # pay_file = request.files ----stuff for image
    payload = request.form.to_dict()
    payload['email'].lower()
    payload['password'] = generate_password_hash(payload['password'])
    query = models.User.update(**payload).where(models.User.id==id)
    query.execute()
    user = models.User.get_by_id(id)
    user_dict = model_to_dict(user)
    del user_dict['password']

    print(payload, '<-payload', query, '<-query')
    return jsonify(data=user_dict, status={"code": 200, "message": "resource updated successfully"})
    
    # file_picture_path = save_picture(dict_file['file'])
    # payload['image'] = file_picture_path
    # current_user.image = file_picture_path

@user.route('/<id>', methods=["Delete"])
def delete_user(id):
    query = models.User.delete().where(models.User.id==id)
    query.execute()
    return jsonify(data='resource successfully deleted', status={"code": 200, "message": "resource deleted successfully"})

