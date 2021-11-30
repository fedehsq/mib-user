from mib.dao.user_manager import UserManager
from mib.models.user import User
from flask import jsonify


def authenticate(auth):
    """
    Authentication resource for generic user.
    :param auth: a dict with email and password keys.
    :return: the response 200 if credentials are correct, else 401
    """
    user: User = UserManager.retrieve_by_email(auth['email'])
    if user is None:
        response = {
            'status': 'failure',
            'message': 'User not found'
        }
        return jsonify(response), 404
    if user.is_blocked:
        # blocked user
        response_code = 403
        response = {
            'status': 'failure',
            'message': 'Blocked user',
        }
    elif user.authenticate(auth['password']):
        response = {
            'status': 'success',
            'message': 'Operation done',
            'body': user.serialize()
        }
        response_code = 200
    else:
        response = {
            'status': 'failure',
            'message': 'Incorrect credentials',
            'body': user.serialize()
        }
        response_code = 400
    return jsonify(response), response_code