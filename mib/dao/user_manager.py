from werkzeug.wrappers import ResponseStream
from mib.dao.manager import Manager
from mib.models.user import User, db
from sqlalchemy import func
from sqlalchemy.sql.expression import or_


class UserManager(Manager):

    @staticmethod
    def create_user(user: User):
        Manager.create(user=user)

    def get_all_users():
        """ 
        This metod gets from the database 
        all users except for the one with user_email 
        """
        return User.query.all()
    
    # This method retrieves a list of user filtered with searched input
    def get_searched_users(searched_input):
        filtered_users = User.query.filter(or_(\
            func.lower(User.first_name).contains(searched_input.lower()),
            func.lower(User.last_name).contains(searched_input.lower()),
            func.lower(User.email).contains(searched_input.lower()))).all()
        return filtered_users

    @staticmethod
    def retrieve_by_id(id_):
        Manager.check_none(id = id_)
        return User.query.get(id_)

    @staticmethod
    def retrieve_by_email(email):
        Manager.check_none(email = email)
        return User.query.filter(User.email == email).first()

    @staticmethod
    def update_user(user: User):
        Manager.update(user = user)

    @staticmethod
    def delete_user(user: User):
        Manager.delete(user = user)

    @staticmethod
    def delete_user_by_id(id_: int):
        user = UserManager.retrieve_by_id(id_)
        UserManager.delete_user(user)
