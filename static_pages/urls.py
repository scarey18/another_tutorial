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
	path('users/<int:pk>/follow', views.follow, name='follow'),
	path('users/<int:pk>/unfollow', views.unfollow, name='unfollow'),
	path('users/<int:pk>/following', views.following, name='following'),
	path('users/<int:pk>/followers', views.followers, name='followers'),
	path('users/password_reset', views.PasswordReset.as_view(), name='password_reset'),
	path('users/password_reset/done', views.PasswordResetDone.as_view(), name='password_reset_done'),
	path('users/password_reset/confirm/<slug:uidb64>/<slug:token>', views.PasswordResetConfirm.as_view(), name='password_reset_confirm'),
	path('login', views.LoginView.as_view(), name='login'),
	path('logout', views.logout, name='logout'),
	path('activate', views.activate, name='activate'),
	path('posts/create', views.create_micropost, name='create_micropost'),
	path('posts/<int:pk>/delete', views.delete_micropost, name='delete_micropost'),
]