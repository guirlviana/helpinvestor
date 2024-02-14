from django.test import TestCase
from core.usecases.investor_usecase import create_user



class CreateUserTests(TestCase):
    def test_should_create_user(self):
        data = {
            'name': 'John',
            'last_name': 'Doe',
            'phone': '11 99999-9999',
            'email': 'johndoe@gmail.com',
            'password': 'j0hND000e'
        }
        
        new_investor = create_user(**data)

        self.assertEqual(data['name'], new_investor.name)
        self.assertEqual(data['last_name'], new_investor.last_name)
        self.assertEqual(data['phone'], new_investor.phone)
        self.assertEqual(data['email'], new_investor.user.email)
        self.assertTrue(new_investor.user.check_password(data['password']))