from flask import request, jsonify
from mib.dao.user_manager import UserManager
from mib.dao.badword_manager import BadWordManager
from mib.dao.blacklist_manager import BlacklistManager
from mib.models.user import User
from mib.models.blacklist import Blacklist
from mib.models.badword import BadWord
from datetime import datetime


def create_user():
    """
    This method allows the creation of a new user.
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
    birthday = datetime.strptime(post_data.get('birthdate'), '%d/%m/%Y')
    user.set_email(email)
    user.set_password(password)
    user.set_first_name(post_data.get('firstname'))
    user.set_last_name(post_data.get('lastname'))
    user.set_birthday(birthday)
    user.set_photo(post_data.get('photo'))
    UserManager.create_user(user)

    # badwords for user
    badwords = post_data.get('badwords').split(', ')
    for word in badwords:
        badword = BadWord()
        badword.word = word
        badword.user_id = user.id
        BadWordManager.create_badword(badword)

    response_object = {
        'user': user.serialize(),
        'status': 'success',
        'message': 'Successfully registered',
    }

    return jsonify(response_object), 201

def edit_user(user_id):
    """
        This method allows the edit of a user.
    """
    post_data = request.get_json()
    user = UserManager.retrieve_by_id(user_id)
    if user is None:
        response = {'status': 'User not present'}
        return jsonify(response), 404
    birthday = datetime.strptime(post_data.get('birthdate'), '%d/%m/%Y')
    user.set_password(post_data.get('password'))
    user.set_first_name(post_data.get('firstname'))
    user.set_last_name(post_data.get('lastname'))
    user.set_birthday(birthday)
    user.set_photo(post_data.get('photo'))
    UserManager.update_user(user)

    # delete all old badwords
    badwords = BadWordManager.retrieve_badwords_by_user_id(user.id)
    for word in badwords:
        BadWordManager.delete_badword(word)

    # inserts new badwords
    badwords = post_data.get('badwords').split(', ')
    if badwords[0] != '':
        for word in badwords:
            badword = BadWord()
            badword.word = word
            badword.user_id = user.id
            BadWordManager.create_badword(badword)

    # delete all old blacklisted users
    blacklist = BlacklistManager.retrieve_by_user_id(user.id)
    for person in blacklist:
        BlacklistManager.delete_blacklisted(person)
    
    # insert the updated blacklisted users
    blacklist = post_data.get('blacklist').split(', ')
    if blacklist[0] != '':
        for person in blacklist:
            blacklist = Blacklist()
            blacklisted = (UserManager.retrieve_by_email(person))
            if blacklisted != None:
                blacklist.id_blacklisted = blacklisted.id
                blacklist.id_user = user.id
                BlacklistManager.create_blacklist(blacklist)
            
    response_object = {
        'user': user.serialize(),
        'status': 'success',
        'message': 'Successfully updated',
    }
    return jsonify(response_object), 200


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

def get_badwords(user_id):
    """
    Get user's badwords by its current id.

    :param user_id: user it
    :return: json response
    """
    user = UserManager.retrieve_by_id(user_id)
    if user is None:
        response = {'status': 'User not present'}
        return jsonify(response), 404
    badwords = BadWordManager.retrieve_badwords_by_user_id(user_id)
    response_object = {
        'badwords': [word.serialize() for word in badwords],
        'status': 'success',
    }
    return jsonify(response_object), 200

def get_blacklist(user_id):
    """
    Get user's blacklist by its current id.

    :param user_id: user it
    :return: json response
    """
    blacklist = BlacklistManager.retrieve_by_user_id(user_id)
    # For each blacklisted user id, get the user object and the response status
    response_object = {
        'blacklist': [(UserManager.retrieve_by_id(person.id_blacklisted)).serialize() for person in blacklist],
        'status': 'success',
    }
    print(response_object)
    return jsonify(response_object), 200


# Get the list of registered users to be retrieved from API gateway
def get_all_users():
    # get all users from db
    users = UserManager.get_all_users()
    # create the response with the list of users 
    return jsonify(users_response = [user.serialize() for user in users]), 200


# Get the list of users corresponding to the searched input to be retrieved
# from API gateway
def get_searched_users(searched_input):
    # get the filtered list
    users = UserManager.get_searched_users(searched_input)
    """if users is None:
        response = {'status': 'There are no users registered'}
        return jsonify(response), 404"""

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
