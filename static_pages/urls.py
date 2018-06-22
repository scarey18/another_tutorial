from django.urls import path

from . import views


app_name = 'static_pages'

urlpatterns = [
	path('home', views.home, name='home'),
	path('help', views.help, name='help'),
]