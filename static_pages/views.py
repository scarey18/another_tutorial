from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.views.generic import DetailView
from django.urls import reverse, reverse_lazy
from django.core.exceptions import ValidationError
from django.contrib import messages, auth
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required

from .models import User
from .utils import parse_error


class UserProfile(LoginRequiredMixin, DetailView):
	model = User
	template_name = 'static_pages/profile.html'
	fields = ['username', 'email']


def home(request):
	return render(request, 'static_pages/home.html')

def help(request):
	return render(request, 'static_pages/help.html', {'page_title': 'Help'})

def about(request):
	return render(request, 'static_pages/about.html', {'page_title': 'About'})

def contact(request):
	return render(request, 'static_pages/contact.html', {'page_title': 'Contact'})

def signup(request):
	context = {'page_title': 'Sign up'}

	if request.method == "POST":
		username = request.POST['username']
		email = request.POST['email']
		password = request.POST['password']
		confirmation = request.POST['confirm_password']
		context['username'], context['email'] = username, email

		if confirmation != password:
			context['error'] = 'Make sure both password fields match.'
			return render(request, 'static_pages/signup.html', context)

		try:
			user = User.objects.create(username=username, email=email, password=password)
		except ValidationError as e:
			context['error'] = parse_error(e)
			return render(request, 'static_pages/signup.html', context)
		else:
			auth.login(request, user)
			messages.success(request, f"Welcome to the Sample App, {user.username}!")
			return HttpResponseRedirect(reverse('static_pages:profile', args=(user.pk,)))

	return render(request, 'static_pages/signup.html', context)

def login(request):
	context = {'page_title': 'Log in'}

	if request.method == 'GET':
		context['next_url'] = request.GET.get('next', '')
		return render(request, 'static_pages/login.html', context)

	elif request.method == 'POST':
		username = request.POST['username']
		password = request.POST['password']
		next_url = request.POST['next']
		user = auth.authenticate(request, username=username, password=password)

		if user is not None:
			auth.login(request, user)
			if next_url:
				return HttpResponseRedirect(next_url)
			else:
				return HttpResponseRedirect(reverse('static_pages:profile', args=(user.pk,)))
		else:
			messages.error(request, "Invalid username/password combination.")
			context['username'], context['next_url'] = username, next_url
			return render(request, 'static_pages/login.html', context)

def logout(request):
	auth.logout(request)
	return HttpResponseRedirect(reverse_lazy('static_pages:home'))
