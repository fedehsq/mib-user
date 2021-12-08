from mib import db
from mib.models.user import User
from sqlalchemy import ForeignKey

class Blacklist(db.Model):

    __tablename__ = 'Blacklist'            

    id = db.Column(db.Integer, primary_key=True, autoincrement = True)
    # user requester
    id_user = db.Column(db.Integer()) 
    # user in the blacklist
    id_blacklisted = db.Column(db.Integer())  

    def __init__(self, *args, **kw):
        super(Blacklist, self).__init__(*args, **kw)
    
    def serialize(self):
        return self.id_blacklisted