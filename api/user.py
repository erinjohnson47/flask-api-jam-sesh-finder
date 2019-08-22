import models


import os
import sys
import secrets
from PIL import Image

from flask import Blueprint, request, jsonify, url_for, send_file

from flask_bcrypt import generate_password_hash, check_password_hash
from flask_login import login_user, current_user, login_required, logout_user
from playhouse.shortcuts import model_to_dict


user = Blueprint('users', 'user', url_prefix='/user')

def save_picture(form_picture):
    random_hex = secrets.token_hex(8)

    f_name, f_ext = os.path.splitext(form_picture.filename)
    picture_name = random_hex + f_ext
    file_path_for_avatar = os.path.join(os.getcwd(), 'static/profile_pics/' + picture_name)
    output_size = (125, 175)
    i = Image.open(form_picture)
    i.thumbnail(output_size) #set the size accepts a typle with dimensions
    i.save(file_path_for_avatar) #save it to the filepath we created

    return picture_name


@user.route('/register', methods=["POST"])
def register():
    print(request.files, request.form) 
    print(type(request))
    pay_file = request.files
    payload = request.form.to_dict()
    dict_file = pay_file.to_dict()
    print(payload, 'payload', type(payload), 'type')

    payload['email'].lower()
    try:
        models.User.get(models.User.email == payload['email'])
        return jsonify(data={}, status={"code": 401, "message": "A user with that username or email exists"})
    except models.DoesNotExist: 
        payload['password'] = generate_password_hash(payload['password'])
        file_picture_path = save_picture(dict_file['file'])
        payload['image'] = file_picture_path

        user = models.User.create(**payload)
        print(type(user))
        login_user(user)

        current_user.image = file_picture_path

        user_dict = model_to_dict(user)
        print(user_dict)
        print(type(user_dict))

        del user_dict['password']

        return jsonify(data=user_dict, status={"code": 201, "message": "Success"})


@user.route('/login', methods=["POST"])
def login():
    payload = request.get_json()
    print(payload, '<-payload')
    try:
        user = models.User.get(models.User.username == payload['username'])
        user_dict = model_to_dict(user)
        print(user_dict, 'user_dict in login route')
        if(check_password_hash(user_dict['password'], payload['password'])):
            login_user(user)
            del user_dict['password']
            print(current_user, '<-current user')
            print(user_dict, '<-user_dict')
            return jsonify(data=user_dict, status={"code": 200, "message": "Success"})
        else:
            return jsonify(data={}, status={"code": 401, "message": "Username or Password is incorrect"})
    except models.DoesNotExist:
        return jsonify(data={}, status={"code": 401, "message": "Username or Password is incorrect"})

@user.route('/logout', methods=["GET"])
def logout():
    logout_user()
    print('this is the logout route in flask')
    return jsonify(status={"code": 200, "message": "Logged out"})


@user.route('/<id>', methods=["PUT"])
@login_required
def update(id):
    pay_file = request.files
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
    
    file_picture_path = save_picture(dict_file['file'])
    payload['image'] = file_picture_path
    current_user.image = file_picture_path

@user.route('/<id>', methods=["Delete"])
def delete_user(id):
    query = models.User.delete().where(models.User.id==id)
    query.execute()
    return jsonify(data='resource successfully deleted', status={"code": 200, "message": "resource deleted successfully"})

