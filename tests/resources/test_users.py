from .view_test import ViewTest
from faker import Faker
import datetime


class TestUsers(ViewTest):
    faker = Faker('it_IT')

    @staticmethod
    def generate_random_user():
        email = TestUsers.faker.email()
        password = TestUsers.faker.password()
        firstname = TestUsers.faker.first_name()
        lastname = TestUsers.faker.last_name()
        birthdate = TestUsers.faker.date_of_birth().strftime('%d/%m/%Y'),
        photo = TestUsers.faker.file_extension(category = 'image')

        data = {
            'email': email,
            'password' : password,
            'firstname' : firstname,
            'lastname' : lastname,
            'birthdate' : birthdate,
            'photo' : photo
        }
            

        return data


    @classmethod
    def setUpClass(cls):
        super(TestUsers, cls).setUpClass()

    def test_delete_user(self):
        user = self.login_test_user()
        rv = self.client.delete('/user/%d' % user.id)
        assert rv.status_code == 202

    def test_get_user_by_id(self):
        # get a non-existent user
        rv = self.client.get('/user/0')
        assert rv.status_code == 404
        # get an existent user
        user = self.login_test_user()
        rv = self.client.get('/user/%d' % user.id)
        assert rv.status_code == 200

    def test_get_user_by_email(self):
        # get a non-existent user with faked email
        rv = self.client.get('/user_email/%s' % TestUsers.faker.email())
        assert rv.status_code == 404
        # get an existent user
        user = self.login_test_user()
        rv = self.client.get('/user_email/%s' % user.email)
        assert rv.status_code == 200
    
    def test_create_user(self):
        # Creating new user
        data = {
            'email': TestUsers.faker.email(),
            'password': TestUsers.faker.password(),
            'firstname': TestUsers.faker.first_name(),
            'lastname' : TestUsers.faker.last_name(),
            'birthdate' : TestUsers.faker.date_of_birth().strftime('%d/%m/%Y'),
            'photo' : TestUsers.faker.file_extension(category = 'image')
        }

        rv = self.client.post('/user', json=data)
        json_response = rv.json

        print(json_response)

        assert rv.status_code == 201

        #testing the return code 200 - User already exists
        rv = self.client.post('/user', json=data)
        assert rv.status_code == 200
        
    def test_update_profile(self):
        user = self.login_test_user()
        user.firstname = TestUsers.faker.first_name()
        user.lastname = TestUsers.faker.last_name()
        data = user.serialize()
        data["firstname"]=data.pop('first_name')
        data["lastname"]=data.pop('last_name')
        data["password"]=user.password
        data["birthdate"]=user.birthdate.strftime('%d/%m/%Y')
        rv = self.client.put('/user/%d' % user.id, json=data)
        assert rv.status_code == 200

        #Updating not existing user profile
        rv = self.client.put('/user/0', json=data)
        assert rv.status_code == 404

    def test_search_users(self):

        rv = self.client.post('/search_users/%s', )
        
    def test_report(self):
        # Reporting existing user
        user = self.login_test_user()
        rv = self.client.post('/report/%s' % user.email)
        assert rv.status_code == 200

        # Reporting not existing user
        rv = self.client.post('/report/%s' % TestUsers.faker.email())
        assert rv.status_code == 404

    def test_user_email(self):
        user = self.login_test_user()
        rv = self.client.get('/user_email/%s' % user.email)
        assert rv.status_code == 200

        rv = self.client.get('/user_email/%s' % TestUsers.faker.email())
        assert rv.status_code == 404

    def test_users(self):
        # Get users list
        rv = self.client.get('/users')
        assert rv.status_code == 200

    def test_badwords(self):
        user = self.login_test_user()

        # Getting badwords of existing user
        rv = self.client.get('/badwords/%d' % user.id)
        assert rv.status_code == 200

        # Getting badwords of not existing user
        rv = self.client.get('/badwords/%d' % 0)
        assert rv.status_code == 404

        data={
            'badwords': ["hate","evil"]
        }

        rv = self.client.post('/badwords/%d' % user.id, json=data)
        assert rv.status_code == 201
        
        # Updating badwords list for existing user

        data={
            'badwords': ["hate","evil","badword"]
        }

        rv = self.client.put('/badwords/%d' % user.id, json=data)
        assert rv.status_code == 200


        # Updating badwords list for not existing user
        rv = self.client.put('/badwords/0', json=data)
        assert rv.status_code == 404

        # Deleting badwords of existing user
        rv = self.client.delete('/badwords/%d' % user.id)
        assert rv.status_code == 202

        # Deleting badwords of not existing user
        rv = self.client.delete('/badwords/0')
        assert rv.status_code == 404

    def test_blacklist(self):
        #Getting the blacklist of the user
        user = self.login_test_user()
        rv = self.client.get('/blacklist/%d' % user.id)
        assert rv.status_code == 200
        
        #Getting the blacklist of not existing user
        rv = self.client.get('/blacklist/0')
        assert rv.status_code == 404
        
        #Creating blacklist of existing user
        data={
            'blacklist': ["baduser1@test.com","baduser2@test.com"]
        }

        rv = self.client.post('/blacklist/%d' % user.id, json=data)
        assert rv.status_code == 201


        #Creating blacklist of not existing user
        rv = self.client.post('/blacklist/0', json=data)
        assert rv.status_code == 404

        # Updating badwords list for existing user

        data={
            'blacklist': ["baduser1@test.com","baduser2@test.com","baduser3@test.com"]
        }

        rv = self.client.put('/blacklist/%d' % user.id, json=data)
        assert rv.status_code == 200


        # Updating badwords list for not existing user
        rv = self.client.put('/blacklist/0', json=data)
        assert rv.status_code == 404

        # Deleting blacklist of existing user
        rv = self.client.delete('/blacklist/%d' % user.id)
        assert rv.status_code == 202

        # Deleting blacklist of not existing user
        rv = self.client.delete('/blacklist/0')
        assert rv.status_code == 404

    def test_update_points(self):

        # Updating lottery points of existing user
        user = self.login_test_user()       
        rv = self.client.put('/user/updatepoints/%d' % user.id, json = {'user/updatepoints' : 'increase'})
        assert rv.status_code == 200

        # Updating lottery points of not existing user
        rv = self.client.put('/user/updatepoints/0')
        assert rv.status_code == 404



