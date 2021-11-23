from mib import db
from sqlalchemy import ForeignKey

class Blacklist(db.Model):

    __tablename__ = 'Blacklist'            

    id = db.Column(db.Integer, primary_key=True, autoincrement=True) # primary key, autoincremental
    id_user = db.Column(db.Integer(), ForeignKey('user.id')) # the user_id who hold the Blacklist
    id_blacklisted = db.Column(db.Integer(), ForeignKey('user.id'))  # the user in the blacklist

    def __init__(self, *args, **kw):
        super(Blacklist, self).__init__(*args, **kw)
    
    
