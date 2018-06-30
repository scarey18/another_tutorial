from django.test import TestCase
from django.urls import reverse

from .models import *

class SignupViewTests(TestCase):
	'''
	Tests the sign up form for users.
	'''

	def test_valid_user(self):
		data = {
			'username': 'validuser2',
			'email': 'validuser2@hotmail.com',
			'password': 'asdlfksjadlk23',
			'confirm_password': 'asdlfksjadlk23',
		}
		response = self.client.post('/signup', data)
		new_user = User.objects.get(username='validuser2')
		expected_url = reverse('static_pages:profile', args=(new_user.pk,))
		self.assertRedirects(response, expected_url, target_status_code=200)

	def test_password_fields_dont_match(self):
		data = {
			'username': 'username1',
			'email': 'username1@hotmail.com',
			'password': 'asldkfwoei3',
			'confirm_password': 'notpassword',
		}
		response = self.client.post('/signup', data)
		self.assertContains(response, 'Make sure both password fields match.')

	def test_model_validation(self):
		'''
		Tests validation at the model level with an already existing username.
		'''
		User.objects.create(username='test1', email='test1@hotmail.com', password='passtest18')
		data = {
			'username': 'test1',
			'email': 'validuser2@hotmail.com',
			'password': 'asdlfksjadlk23',
			'confirm_password': 'asdlfksjadlk23',
		}
		response = self.client.post('/signup', data)
		self.assertContains(response, 'A user with that username already exists.')