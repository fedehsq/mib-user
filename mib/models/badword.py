from mib import db
from sqlalchemy import ForeignKey

class BadWord(db.Model):
    """
        Representation of BadWord model.
        Bad word table, each instance is associated with user id.
        The word can't be sent to that user
    """
    __tablename__ = 'BadWord'

    id = db.Column(db.Integer, primary_key = True, autoincrement = True)
    # bad word for an user...
    word = db.Column(db.String, nullable = False, unique = False)
    # ... with User.id = 'user_id'
    user_id = db.Column(db.Integer, ForeignKey('User.id'), nullable = False, unique = False)

    def serialize(self):
        #return dict([(k, self.__getattribute__(k)) for k in ['word']])
        return self.word