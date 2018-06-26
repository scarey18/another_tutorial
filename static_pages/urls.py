from django.urls import path

from . import views


app_name = 'static_pages'

urlpatterns = [
	path('', views.home, name='home'),
	path('home', views.home, name='home'),
	path('help', views.help, name='help'),
	path('about', views.about, name='about'),
	path('contact', views.contact, name='contact'),
	path('signup', views.signup, name='signup')
]