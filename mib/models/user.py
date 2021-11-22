from werkzeug.security import generate_password_hash, check_password_hash

from mib import db


class User(db.Model):
    """Representation of User model."""

    # The name of the table that we explicitly set
    __tablename__ = 'User'

    # A list of fields to be serialized
    SERIALIZE_LIST = ['id', 'email', 'is_active', 'authenticated', 'deleted', 'is_blocked']

    # All fields of user
    photo = db.Column(db.Unicode(8196), default = 'profile_pics/profile_pic.svg')
    id = db.Column(db.Integer, primary_key = True, autoincrement = True)
    email = db.Column(db.Unicode(128), nullable = False, unique = True)
    first_name = db.Column(db.Unicode(128), nullable = False, unique = False)
    last_name = db.Column(db.Unicode(128), nullable = False, unique = False)
    password = db.Column(db.Unicode(128))
    birthdate = db.Column(db.DateTime())
    is_active = db.Column(db.Boolean, default = True)
    authenticated = db.Column(db.Boolean, default = True)
    forbidden_words = db.Column(db.Unicode(1024), default = "")
    is_blocked = db.Column(db.Boolean, default = False)
    deleted = db.Column(db.Boolean, default = False)
    # blacklist = db.Column(db.Unicode(1024), default = "")
    # lottery_number = db.Column(db.Integer, default = 0)
    # points = db.Column(db.Integer, default = 0)
    # photo_path = db.Column(db.Unicode(128), default = 'profile_pics/profile_pic.svg')

    def __init__(self, *args, **kw):
        super(User, self).__init__(*args, **kw)
        self.authenticated = False

    def set_password(self, password):
        self.password = generate_password_hash(password)

    def set_email(self, email):
        self.email = email

    def set_first_name(self, name):
        self.first_name = name

    def set_last_name(self, name):
        self.last_name = name

    def is_authenticated(self):
        return self.authenticated

    def set_birthday(self, birthdate):
        self.birthdate = birthdate

    def authenticate(self, password):
        checked = check_password_hash(self.password, password)
        self.authenticated = checked
        return self.authenticated

    def set_photo(self,photo):
        self.photo=photo
        
    def serialize(self):
        return dict([(k, self.__getattribute__(k)) for k in self.SERIALIZE_LIST])
