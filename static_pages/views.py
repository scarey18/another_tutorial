from django.shortcuts import render
from django.http import request, HttpResponse
from django.views.generic import DetailView

from .models import User


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
	return render(request, 'static_pages/signup.html', {'page_title': 'Sign up'})