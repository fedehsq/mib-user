from werkzeug.security import generate_password_hash, check_password_hash

from mib import db


class User(db.Model):
    """
    Representation of User model.
    """

    # The name of the table that we explicitly set
    __tablename__ = 'User'

    # A list of fields to be serialized
    SERIALIZE_LIST = ['id', 'email', 'first_name', 'last_name', 'birthdate', 'photo', 'is_blocked']

    # All fields of user
    photo = db.Column(db.String)
    id = db.Column(db.Integer, primary_key = True, autoincrement = True)
    email = db.Column(db.Unicode(128), nullable = False, unique = True)
    first_name = db.Column(db.Unicode(128), nullable = False, unique = False)
    last_name = db.Column(db.Unicode(128), nullable = False, unique = False)
    password = db.Column(db.Unicode(128))
    birthdate = db.Column(db.DateTime())
    reports = db.Column(db.Integer, default = 0)
    is_blocked = db.Column(db.Boolean, default = False)

    def set_password(self, password):
        self.password = generate_password_hash(password)

    def set_email(self, email):
        self.email = email

    def set_first_name(self, name):
        self.first_name = name

    def set_last_name(self, name):
        self.last_name = name

    def set_birthday(self, birthdate):
        self.birthdate = birthdate

    def authenticate(self, password):
        return check_password_hash(self.password, password)

    def set_photo(self,photo):
        self.photo = photo
        
    def serialize(self):
        return dict([(k, self.__getattribute__(k)) for k in self.SERIALIZE_LIST])