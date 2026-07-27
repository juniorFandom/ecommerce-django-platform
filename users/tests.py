from django.test import TestCase
from django.urls import reverse
from .models import User

# Create your tests here.
class TestUser(TestCase):
    def setUp(self):
        self.user = User(email='test@gmail.com',password='2344')

    def test_create(self):
        url = 'user-create'
        data = {
            'email':'test1@gmail.com',
            'username':'mon_test',
            'first_name':'syxe',
            'last_name':'naomie12',
            'password':'juniro93@@',
            'password_confirm':'juniro93@@'
        }

        result = self.client.post(reverse(url), data=data)
        self.assertEqual(result.status_code, 201)

    def test_instance(self):
            self.assertIsInstance(self.user, User)
    
    def test_update(self):
        url = 'user-create'
        data = {
            'email':'test1@gmail.com',
            'username':'mon_test',
            'first_name':'syxe',
            'last_name':'naomie12',
            'password':'juniro93@@',
            'password_confirm':'juniro93@@'
        }

        result = self.client.post(reverse(url), data=data)
        slug = result.json()['slug']

        url_update='user-update'

        data = {
            'is_active':1
        }

        result_update = self.client.patch(reverse(url_update, args=[slug]), json=data)
        self.assertEqual(result_update.status_code, 200)
    
    def test_list(self):
        url_list = 'user-list'
        result = self.client.get(reverse(url_list))
        self.assertEqual(result.status_code, 200)
    
    def test_delete(self):
        url = 'user-create'
        data = {
            'email':'test1@gmail.com',
            'username':'mon_test',
            'first_name':'syxe',
            'last_name':'naomie12',
            'password':'juniro93@@',
            'password_confirm':'juniro93@@'
        }

        result = self.client.post(reverse(url), data=data)
        slug = result.json()['slug']
        url_delete='user-delete'
        result_update = self.client.delete(reverse(url_delete, args=[slug]))
        self.assertEqual(result_update.status_code, 204)


