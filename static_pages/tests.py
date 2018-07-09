from django.test import TestCase
from django.urls import reverse, reverse_lazy
from django.contrib import auth

from .models import User

SIGNUP_DATA = {
	'username': 'test',
	'email': 'test@testing.com',
	'password1': 'something2018',
	'password2': 'something2018'
}

def new_user():
	return User.objects.create_user(
		username='test',
		email='test@testing.com',
		password='something2018'
	)

##### Views #####

class UserProfileTests(TestCase):
	def test_user_profile_logged_in(self):
		user = new_user()
		self.client.login(username='test', password='something2018')
		resp = self.client.get(reverse('static_pages:profile', args=(user.pk,)))
		self.assertEqual(resp.status_code, 200)
		self.assertEqual(resp.context['user'], user)
		self.assertEqual(resp.context['page_title'], user.username)

	def test_user_profile_not_logged_in(self):
		user = new_user()
		resp = self.client.get(reverse('static_pages:profile', args=(user.pk,)))
		self.assertEqual(resp.status_code, 302)
		self.assertEqual(resp['Location'], '/login?next=/users/1')


class SignupViewTests(TestCase):
	def test_signup_view(self):
		resp = self.client.get(reverse_lazy('static_pages:signup'))
		self.assertEqual(resp.status_code, 200)
		self.assertEqual(resp.context['page_title'], 'Sign up')

	def test_signup_form_valid(self):
		resp = self.client.post(reverse_lazy('static_pages:signup'), SIGNUP_DATA, follow=True)
		user = auth.get_user(self.client)
		self.assertEqual(resp.status_code, 200)
		self.assertEqual(resp.context['page_title'], 'test')
		self.assertContains(resp, 'Welcome to the Sample App, test!')
		self.assertEqual(user.username, 'test')
