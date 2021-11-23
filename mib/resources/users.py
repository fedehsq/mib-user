from flask import request, jsonify
from mib.dao.user_manager import UserManager
from mib.models.user import User
import datetime


def create_user():
    """This method allows the creation of a new user.
    """
    post_data = request.get_json()
    email = post_data.get('email')
    password = post_data.get('password')

    searched_user = UserManager.retrieve_by_email(email)
    if searched_user is not None:
        return jsonify({
            'status': 'Already present'
        }), 200

    user = User()
    birthday = datetime.datetime.strptime(post_data.get('birthdate'), '%Y-%m-%d')
    user.set_email(email)
    user.set_password(password)
    user.set_first_name(post_data.get('firstname'))
    user.set_last_name(post_data.get('lastname'))
    user.set_birthday(post_data.get('birthdate'))
    user.set_photo(post_data.get('photo'))

    UserManager.create_user(user)

    response_object = {
        'user': user.serialize(),
        'status': 'success',
        'message': 'Successfully registered',
    }

    return jsonify(response_object), 201


def get_user(user_id):
    """
    Get a user by its current id.

    :param user_id: user it
    :return: json response
    """
    user = UserManager.retrieve_by_id(user_id)
    if user is None:
        response = {'status': 'User not present'}
        return jsonify(response), 404

    return jsonify(user.serialize()), 200

# Get the list of users corresponding to the searched input to be retrieved
# from API gateway
def get_searched_users(searched_input):
    # get the filtered list
    users = UserManager.get_searched_users(searched_input)
    print(users)

    if users is None:
        response = {'status': 'There are no users registered'}
        return jsonify(response), 404

    # create the response with the filtered list of users 
    return jsonify(searched_users = [user.serialize() for user in users]), 200

# Report a user, if it exists
# If not so, get a 404 response to the API gateway
def report(email):
    reported_user = UserManager.report(email)
    # if reported_user returned from the function is None, it means
    # that the email doesn't correspond to anyone
    if reported_user is None:
        response = {'status': 'There are no users registered with this email'}
        return jsonify(response), 404
    else:
        # create the response with the reported users 
        return jsonify(reported_user.serialize()), 200
    


# Get the list of registered users to be retrieved from API gateway
def get_all_users():
    # get all users from db
    users = UserManager.get_all_users()
 
    if users is None:
        response = {'status': 'There are no users registered'}
        return jsonify(response), 404
    # create the response with the list of users 
    return jsonify(users_response = [user.serialize() for user in users]), 200

def get_user_by_email(user_email):
    """
    Get a user by its current email.

    :param user_email: user email
    :return: json response
    """
    user = UserManager.retrieve_by_email(user_email)
    if user is None:
        response = {'status': 'User not present'}
        return jsonify(response), 404

    return jsonify(user.serialize()), 200


def delete_user(user_id):
    """
    Delete the user with id = user_id.

    :param user_id the id of user to be deleted
    :return json response
    """
    UserManager.delete_user_by_id(user_id)
    response_object = {
        'status': 'success',
        'message': 'Successfully deleted',
    }

    return jsonify(response_object), 202
