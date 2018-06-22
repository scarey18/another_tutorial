from django.shortcuts import render
from django.http import request, HttpResponse


def home(request):
	return render(request, 'static_pages/home.html', {'page_title': 'Home'})

def help(request):
	return render(request, 'static_pages/help.html', {'page_title': 'Help'})

def about(request):
	return render(request, 'static_pages/about.html', {'page_title': 'About'})

def contact(request):
	return render(request, 'static_pages/contact.html', {'page_title': 'Contact'})