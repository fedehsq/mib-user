from werkzeug.wrappers import ResponseStream
from mib.dao.manager import Manager
from mib.models.blacklist import Blacklist, db


class BlacklistManager(Manager):

    @staticmethod
    def add_blacklisted(blacklisted: Blacklist):
        """
        Add a row to the blacklist table
        """
        Manager.create(blacklisted = blacklisted)

    @staticmethod
    def retrieve_by_user_id(id_user):
        """
        Get all blacklisted users for the user corresponding to id_user
        """
        Manager.check_none(id_user = id_user)
        return Blacklist.query.get(id_user)
    
    @staticmethod
    def delete_blacklisted(blacklisted: Blacklist):
        """
        Delete a row in the blacklist table
        """
        Manager.delete(blacklisted = blacklisted)
    
    @staticmethod
    def delete_all_by_user_id(id_user):
        """
        Delete all blacklisted users for the user corresponding to id_user
        """
        for blacklisted in Manager.retrieve_by_user_id(id_user):
            Manager.delete_blacklisted(blacklisted)



