from .view_test import ViewTest
from faker import Faker


class TestAuth(ViewTest):

    faker = Faker('it_IT')

    @classmethod
    def setUpClass(cls):
        super(TestAuth, cls).setUpClass()

    def test_login(self):
        # login for a customer
        user = self.login_test_user()

        #login with wrong email (not existing user)
        data = {
            'email': TestAuth.faker.email(),
            'password': TestAuth.faker.password()
        }

        response = self.client.post('/authenticate', json=data)
        json_response = response.json

        assert response.status_code == 404
        assert json_response["status"] == 'failure'
        assert json_response['message'] == 'User not found'

        # login with a wrong password (incorrect credentials)
        data = {
            'email': user.email,
            'password': TestAuth.faker.password()
        }

        response = self.client.post('/authenticate', json=data)
        json_response = response.json

        assert response.status_code == 400
        assert json_response["status"] == 'failure'
        assert json_response['message'] == 'Incorrect credentials'

        #login for a blocked user
        user.is_blocked = True
        data = {
            'email' : user.email,
            'password' : user.password,
            'is_blocked' : user.is_blocked
        }
        response = self.client.post('/authenticate', json=data)
        json_response = response.json
    
        assert response.status_code == 403
        assert json_response["status"] == 'failure'
        assert json_response['message'] == 'Blocked user'






    
    


