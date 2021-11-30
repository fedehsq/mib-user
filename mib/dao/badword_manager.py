from mib.dao.manager import Manager
from mib.models.user import User
from mib.models.badword import BadWord


class BadWordManager(Manager):

    @staticmethod
    def retrieve_badwords_by_user_id(id_):
        """
        :param id_: user's id
        Given the user id 'id_', returns all his badwords.
        """
        Manager.check_none(id=id_)
       # return User.query.filter(User.email == email).first()

        return BadWord.query.filter(BadWord.user_id == id_).all()

    @staticmethod
    def create_badword(badword: BadWord):
        """
        :param word: badword
        :param id_: user's id
        Given the badword 'word' and the user id 'id_', add word to user's badwords.
        """
        Manager.create(badword = badword)

    
    @staticmethod
    def create_badwords_by_user_id(id, badwords):
        """
        :param word: badwords
        :param id_: user's id
        Given the badwords add them to ser's badwords.
        """
        if badwords[0] != '':
            for word in badwords:
                badword = BadWord()
                badword.word = word
                badword.user_id = id
                BadWordManager.create_badword(badword)

    


    @staticmethod
    def delete_badword(badword: BadWord):
        Manager.delete(badword=badword)