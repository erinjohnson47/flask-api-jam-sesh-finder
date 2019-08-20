import models


import os
import sys
import secrets
# from PIL import Image

from flask import Blueprint, request, jsonify, url_for, send_file

from flask_bcrypt import generate_password_hash, check_password_hash
from flask_login import login_user, current_user
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





