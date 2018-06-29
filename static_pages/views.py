from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.views.generic import DetailView
from django.urls import reverse
from django.core.exceptions import ValidationError

from .models import User
from .utils import parse_error


class UserProfile(DetailView):
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
	if request.method == "POST":
		username = request.POST['username']
		email = request.POST['email']
		password = request.POST['password']
		confirmation = request.POST['confirm_password']
		context = {
			'page_title': 'Sign up',
			'username': username,
			'email': email,
		}

		if confirmation != password:
			context['error'] = 'Make sure both password fields match.'
			return render(request, 'static_pages/signup.html', context)

		try:
			user = User.objects.create(username=username, email=email, password=password)
		except ValidationError as e:
			context['error'] = parse_error(e)
			return render(request, 'static_pages/signup.html', context)

		return HttpResponseRedirect(reverse('static_pages:profile', args=(user.pk,)))

	return render(request, 'static_pages/signup.html', {'page_title': 'Sign up'})