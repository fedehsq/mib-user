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
    Returns the new user
    """
    post_data = request.get_json()
    email = post_data.get('email')
    password = post_data.get('password')

    searched_user = UserManager.retrieve_by_email(email)
    if searched_user is not None:
        return jsonify({
            'status': 'failure',
            'message': 'User already exists'
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

    """# badwords for user
    badwords = post_data.get('badwords').split(', ')
    BadWordManager.create_badwords_by_user_id(user.id, badwords)
    for word in badwords:
        badword = BadWord()
        badword.word = word
        badword.user_id = user.id
        BadWordManager.create_badword(badword)"""

    response_object = {
        'status': 'success',
        'message': 'Operarion done',
        'body': user.serialize(),
    }

    return jsonify(response_object), 201

def create_badwords(user_id):
    """
    This method allows the creation of the badword for the user with user_id.
    Returns the list of badwords
    """
    user = UserManager.retrieve_by_id(user_id)
    if user is None:
        return jsonify({
            'status': 'failure',
            'message': 'User not found'
        }), 404

    # badwords for user
    post_data = request.get_json()
    badwords = post_data.get('badwords')
    BadWordManager.create_badwords_by_user_id(user.id, badwords)
    response_object = {
        'status': 'success',
        'message': 'Operation done',
        'body': badwords,
    }
    return jsonify(response_object), 201

def update_badwords(user_id): 
    """
    This method allows the update of the badword for the user with user_id.
    Returns the list of badwords
    """
    delete_badwords(user_id)
    response, code = create_badwords(user_id)
    return response, 200 if code != 404 else code

def create_blacklist(user_id):
    """
    This method allows the creation of the blacklist for the user with user_id.
    Returns the blacklist
    """
    user = UserManager.retrieve_by_id(user_id)
    if user is None:
        return jsonify({
            'status': 'failure',
            'message': 'User not found'
        }), 404
    post_data = request.get_json()
    # Create the blacklist for the user
    blacklist = post_data.get('blacklist')
    bl = []

    if blacklist[0] != '':
        for person in blacklist:
            blacklist = Blacklist()
            blacklisted = (UserManager.retrieve_by_email(person))
            if blacklisted != None:
                blacklist.id_blacklisted = blacklisted.id
                blacklist.id_user = user.id
                BlacklistManager.create_blacklist(blacklist)
                bl.append(blacklisted)

    response_object = {
        'status': 'success',
        'message': 'Operation done',
        'body': [person.email for person in bl],
    }
    return jsonify(response_object), 201
    
def update_blacklist(user_id):
    """
    This method allows the update of the blacklist for the user with user_id.
    Returns the blacklist
    """
    delete_blacklist(user_id)
   # BlacklistManager.delete_blacklisted(user_id)
    response, code = create_blacklist(user_id)
    return response, 200 if code != 404 else code

def edit_user(user_id):
    """
    This method allows the edit of a user.
    Returns the updated user
    """
    post_data = request.get_json()
    user = UserManager.retrieve_by_id(user_id)
    if user is None:
        response = {
            'status': 'failure',
            'message': 'User not found'
        }
        return jsonify(response), 404
    birthday = datetime.strptime(post_data.get('birthdate'), '%d/%m/%Y')
    user.set_password(post_data.get('password'))
    user.set_first_name(post_data.get('firstname'))
    user.set_last_name(post_data.get('lastname'))
    user.set_birthday(birthday)
    user.set_photo(post_data.get('photo'))
    UserManager.update_user(user)
    response_object = {
        'status': 'success',
        'message': 'Successfully updated',
        'body': user.serialize(),
    }
    return jsonify(response_object), 200


def get_user(user_id):
    """
    Get a user by its current id.
    :param user_id: user id
    :return: the user
    """
    user = UserManager.retrieve_by_id(user_id)
    if user is None:
        response = {
            'status': 'failure',
            'message': 'User not found'
        }
        return jsonify(response), 404
    response_object = {
        'status': 'success',
        'message': 'Successfully got',
        'body': user.serialize(),
    }
    return jsonify(response_object), 200

def get_badwords(user_id):
    """
    Get user's badwords by its current id.

    :param user_id: user id
    :return: badwords list
    """
    user = UserManager.retrieve_by_id(user_id)
    if user is None:
        response = {
            'status': 'failure',
            'message': 'User not found'
        }
        return jsonify(response), 404
    badwords = BadWordManager.retrieve_badwords_by_user_id(user_id)
    response_object = {
        'status': 'success',
        'message': 'Operation done',
        'body': [word.serialize() for word in badwords],
    }
    return jsonify(response_object), 200

def get_blacklist(user_id):
    """
    Get user's blacklist by its current id.
    :param user_id: user id
    :return: blacklist
    """
    user = UserManager.retrieve_by_id(user_id)
    if user is None:
        response = {
            'status': 'failure',
            'message': 'User not found'
        }
        return jsonify(response), 404

    blacklist = BlacklistManager.retrieve_by_user_id(user_id)
    # For each blacklisted user id, get the user object and the response status
    response_object = {
        'status': 'success',
        'message': 'Operation done',
        'body': [(UserManager.retrieve_by_id(person.id_blacklisted)).email for person in blacklist],
    }
    return jsonify(response_object), 200

def get_searched_users(searched_input):
    """
    Returns the list of users matching to the searched input
    """
    # get the filtered list
    users = UserManager.get_searched_users(searched_input)
    """if users is None:
        response = {'status': 'There are no users registered'}
        return jsonify(response), 404"""

    # create the response with the filtered list of users 
    response_object = {
        'status': 'success',
        'message': 'Operation done',
        'body': [user.serialize() for user in users],
    }
    return jsonify(response_object), 200

def report(email):
    """
    Reports a user, if it exists
    """
    user = UserManager.retrieve_by_email(email)
    if user is None:
        response = {
            'status': 'failure',
            'Message': 'User not found'
        }
        return jsonify(response), 404
    user.reports += 1
    # check if report number is >= 3, 
    # so the user will be blocked and it can't login anymore
    user.is_blocked = user.reports >= 3
    UserManager.update_user(user)
    # create the response with the reported users
    response_object = {
        'status': 'success',
        'message': 'User reported',
    }
    return jsonify(response_object), 200
    
def get_all_users():
    """
    Returns the list of registered users 
    """
    # get all users from db
    users = UserManager.get_all_users()
    # create the response with the list of users
    response_object = {
        'status': 'success',
        'message': 'Operation done',
        'body': [user.serialize() for user in users],
    }
    return jsonify(response_object), 200

def get_user_by_email(user_email):
    """
    Get a user by its current email.
    :param user_email: user email
    :return: the user
    """
    user = UserManager.retrieve_by_email(user_email)
    if user is None:
        response = {
            'status': 'failure',
            'message': 'User not found'
        }
        return jsonify(response), 404
    response_object = {
        'status': 'success',
        'message': 'Operation done',
        'body': user.serialize(),
    }
    return jsonify(response_object), 200

def delete_blacklist(user_id):
    """
    Delete the blacklist of the user with id = user_id.
    :param user_id the id of user whose blacklist has to be deleted
    return the result of the operation
    """
    user = UserManager.retrieve_by_id(user_id)
    if user is None:
        response = {
            'status': 'failure',
            'message': 'User not found'
        }
        return jsonify(response), 404
    
    # delete blacklist
    blacklist = BlacklistManager.retrieve_by_user_id(user.id)
    for person in blacklist:
        BlacklistManager.delete_blacklisted(person)
    response_object = {
        'status': 'success',
        'message': 'Successfully deleted',
    }
    return jsonify(response_object), 202

def delete_badwords(user_id):
    """
    Delete the user with id = user_id.
    :param user_id the id of user whose badwords have to be deleted
    :return the result of the operation
    """
    user = UserManager.retrieve_by_id(user_id)
    if user is None:
        response = {
            'status': 'failure',
            'message': 'User not found'
        }
        return jsonify(response), 404
    # delete all old badwords
    badwords = BadWordManager.retrieve_badwords_by_user_id(user.id)
    for word in badwords:
        BadWordManager.delete_badword(word)    
    response_object = {
        'status': 'success',
        'message': 'Successfully deleted',
    }
    return jsonify(response_object), 202

def delete_user(user_id):
    """
    Delete the user with id = user_id.
    :param user_id the id of user to be deleted
    :return the result of the operation
    """
    user = UserManager.retrieve_by_id(user_id)
    if user is None:
        response = {
            'status': 'failure',
            'message': 'User not found'
        }
        return jsonify(response), 404
    UserManager.delete_user_by_id(user_id)
    response_object = {
        'status': 'success',
        'message': 'Successfully deleted',
    }
    return jsonify(response_object), 202