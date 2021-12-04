import unittest

from faker import Faker

from .model_test import ModelTest


class TestUser(ModelTest):

    faker = Faker()

    @classmethod
    def setUpClass(cls):
        super(TestUser, cls).setUpClass()

        from mib.models import user
        cls.user = user

    @staticmethod
    def assertUserEquals(value, expected):
        t = unittest.FunctionTestCase(TestUser)
        t.assertEqual(value.email, expected.email)
        t.assertEqual(value.password, expected.password)
        t.assertEqual(value.first_name, expected.first_name)
        t.assertEqual(value.last_name, expected.last_name)
        #t.assertEqual(value.is_active, expected.is_active)
        #t.assertEqual(value.authenticated, False)
        #t.assertEqual(value.is_anonymous, expected.is_anonymous)

    @staticmethod
    def generate_random_user():
        email = TestUser.faker.email()
        password = TestUser.faker.password()
        first_name = TestUser.faker.first_name()
        last_name = TestUser.faker.last_name()
        birthdate = TestUser.faker.date_time()
        photo = TestUser.faker.file_extension(category = 'image')
        #is_active = TestUser.faker.boolean()
        #is_admin = TestUser.faker.boolean()
        #authenticated = TestUser.faker.boolean()
        #is_anonymous = TestUser.faker.boolean()
        #phone = TestUser.faker.phone_number()

        from mib.models import User

        user = User(
            email=email,
            password=password,
            #is_active=is_active,
            #is_admin=is_admin,
            #authenticated=authenticated,
            #is_anonymous=is_anonymous,
            first_name=first_name,
            last_name=last_name,
            birthdate = birthdate,
            photo = photo
            #reports=reports,
            #is_blocked = is_blocked
            #phone=phone,
        )

        return user

    def test_set_password(self):
        user = TestUser.generate_random_user()
        password = self.faker.password(length=10, special_chars=False, upper_case=False)
        user.set_password(password)

        self.assertEqual(
            user.authenticate(password),
            True
        )
    
    def test_set_email(self):
        user = TestUser.generate_random_user()
        email = self.faker.email()
        user.set_email(email)
        self.assertEqual(email, user.email)

    def test_set_first_name(self):
        user = TestUser.generate_random_user()
        first_name = self.faker.first_name()
        user.set_first_name(first_name)
        self.assertEqual(first_name, user.first_name)

    def test_set_last_name(self):
        user = TestUser.generate_random_user()
        last_name = self.faker.last_name()
        user.set_last_name(last_name)
        self.assertEqual(last_name, user.last_name)
    
    def test_set_birthday(self):
        user = TestUser.generate_random_user()
        birthdate = self.faker.date_time()
        user.set_birthday(birthdate)
        self.assertEqual(birthdate,user.birthdate)

    def test_set_photo(self):
        user = TestUser.generate_random_user()
        photo = self.faker.file_extension(category = 'image')
        user.set_photo(photo)
        self.assertEqual(photo,user.photo)

'''   def test_is_authenticated(self):
        user = TestUser.generate_random_user()
        self.assertFalse(user.is_authenticated())
'''
