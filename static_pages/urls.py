from django.urls import path, include
from django.contrib.auth import views as auth_views

from . import views


app_name = 'static_pages'

urlpatterns = [
	path('', views.home, name='home'),
	path('help', views.help, name='help'),
	path('about', views.about, name='about'),
	path('contact', views.contact, name='contact'),
	path('signup', views.SignupView.as_view(), name='signup'),
	path('users', views.IndexView.as_view(), name='index'),
	path('users/<int:pk>', views.UserProfile.as_view(), name='profile'),
	path('users/<int:pk>/edit', views.EditUser.as_view(), name='edit_user'),
	path('users/<int:pk>/deactivate', views.deactivate, name='deactivate'),
	path('login', views.LoginView.as_view(), name='login'),
	path('logout', views.logout, name='logout'),
]