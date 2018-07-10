from django.test import TestCase
from django.urls import reverse, reverse_lazy
from django.contrib import auth
from django.contrib.auth.models import AnonymousUser

from .models import User


def new_user():
	return User.objects.create_user(
		username='test',
		email='test@testing.com',
		password='something2018'
	)

##### VIEW TESTS #####

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
		data = {
			'username': 'test',
			'email': 'test@testing.com',
			'password1': 'something2018',
			'password2': 'something2018'
		}
		resp = self.client.post(reverse_lazy('static_pages:signup'), data, follow=True)
		user = auth.get_user(self.client)
		self.assertEqual(resp.status_code, 200)
		self.assertEqual(resp.context['page_title'], 'test')
		self.assertContains(resp, 'Welcome to the Sample App, test!')
		self.assertEqual(user.username, 'test')


class LoginViewTests(TestCase):
	def test_login_view(self):
		resp = self.client.get(reverse_lazy('static_pages:login'))
		self.assertEqual(resp.status_code, 200)
		self.assertEqual(resp.context['page_title'], 'Log in')

	def test_login_form_valid(self):
		user = new_user()
		data = {'username': 'test', 'password': 'something2018', 'remember_me': 'on'}
		resp = self.client.post(reverse_lazy('static_pages:login'), data)
		self.assertEqual(resp.status_code, 302)
		self.assertEqual(resp.url, '/')
		self.assertEqual(user, auth.get_user(self.client))

	def test_login_form_valid_with_next_url(self):
		user = new_user()
		data = {'username': 'test', 'password': 'something2018', 'next': '/users/1'}
		resp = self.client.post(reverse_lazy('static_pages:login'), data)
		self.assertEqual(resp.status_code, 302)
		self.assertEqual(resp.url, '/users/1')


class HomeViewTests(TestCase):
	def test_home_view(self):
		resp = self.client.get(reverse_lazy('static_pages:home'))
		self.assertEqual(resp.status_code, 200)


class HelpViewTests(TestCase):
	def test_help_view(self):
		resp = self.client.get(reverse_lazy('static_pages:help'))
		self.assertEqual(resp.status_code, 200)
		self.assertEqual(resp.context['page_title'], 'Help')


class AboutViewTests(TestCase):
	def test_about_view(self):
		resp = self.client.get(reverse_lazy('static_pages:about'))
		self.assertEqual(resp.status_code, 200)
		self.assertEqual(resp.context['page_title'], 'About')


class ContactViewTests(TestCase):
	def test_contact_view(self):
		resp = self.client.get(reverse_lazy('static_pages:contact'))
		self.assertEqual(resp.status_code, 200)
		self.assertEqual(resp.context['page_title'], 'Contact')


class LogoutViewTests(TestCase):
	def test_logout_view(self):
		user = new_user()
		self.client.login(username='test', password='something2018')
		resp = self.client.get(reverse_lazy('static_pages:logout'))
		self.assertEqual(resp.status_code, 302)
		self.assertEqual(resp.url, '/')
		self.assertIsInstance(auth.get_user(self.client), AnonymousUser)