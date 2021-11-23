from werkzeug.wrappers import ResponseStream
from mib.dao.manager import Manager
from mib.models.user import User, db


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
        tmp = []
        users = User.query.all() 
        # for each user search if the searched input is in the email, or firstname or lastname
        # if so, save the user in tmp
        for u in users:
            if searched_input.lower() in u.first_name.lower() or searched_input.lower() in u.last_name.lower() or searched_input.lower() in u.email.lower():
                tmp.append(u)
        return tmp

    # This method reports and returns the user corresponding to email, if it exists
    def report(email):
        reported_user = User.query.filter(User.email == email).first()
        if reported_user != None:
            reported_user.reports += 1
            print("NUM REPORTS:")
            print(reported_user.reports)
            # check if report number is 3, so the user will be blocked and can't login anymore
            if reported_user.reports == 3:
                reported_user.is_blocked = True
            db.session.commit()
        return reported_user

    @staticmethod
    def retrieve_by_id(id_):
        Manager.check_none(id=id_)
        return User.query.get(id_)

    @staticmethod
    def retrieve_by_email(email):
        Manager.check_none(email=email)
        return User.query.filter(User.email == email).first()

    @staticmethod
    def update_user(user: User):
        Manager.update(user=user)

    @staticmethod
    def delete_user(user: User):
        Manager.delete(user=user)

    @staticmethod
    def delete_user_by_id(id_: int):
        user = UserManager.retrieve_by_id(id_)
        UserManager.delete_user(user)
