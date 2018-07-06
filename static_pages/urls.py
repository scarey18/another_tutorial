from django.urls import path, include

from . import views


app_name = 'static_pages'

urlpatterns = [
	path('', views.home, name='home'),
	path('help', views.help, name='help'),
	path('about', views.about, name='about'),
	path('contact', views.contact, name='contact'),
	path('signup', views.signup, name='signup'),
	path('users/<int:pk>', views.UserProfile.as_view(), name='profile'),
	path('login', views.login, name='login'),
	path('logout', views.logout, name='logout'),
]