from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.views.generic import DetailView, CreateView
from django.urls import reverse, reverse_lazy
from django.core.exceptions import ValidationError
from django.contrib import messages, auth
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView

from .models import User
from .utils import parse_error
from .forms import UserForm

class UserProfile(LoginRequiredMixin, DetailView):
	model = User
	template_name = 'static_pages/profile.html'
	fields = ['username', 'email']

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		context['page_title'] = context['user'].username
		return context


class SignupView(CreateView):
	model = User
	template_name = 'static_pages/signup.html'
	form_class = UserForm

	def form_valid(self, form):
		new_user = form.save()
		auth.login(self.request, new_user)
		self.request.session.set_expiry(0)
		messages.success(
			self.request,
			f"Welcome to the Sample App, {new_user.username}!"
		)
		return HttpResponseRedirect(new_user.get_absolute_url())

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		context['page_title'] = 'Sign up'
		return context


class LoginView(LoginView):
	template_name = 'static_pages/login.html'
	extra_context = {'page_title': 'Log in'}

	def form_valid(self, form):
		user = form.get_user()
		next_url = self.request.POST.get('next', '')
		auth.login(self.request, user)

		if self.request.POST.get('remember_me', False) is False:
			self.request.session.set_expiry(0)

		return HttpResponseRedirect(next_url) if next_url else\
			HttpResponseRedirect(reverse_lazy('static_pages:home'))


def home(request):
	return render(request, 'static_pages/home.html')

def help(request):
	return render(request, 'static_pages/help.html', {'page_title': 'Help'})

def about(request):
	return render(request, 'static_pages/about.html', {'page_title': 'About'})

def contact(request):
	return render(request, 'static_pages/contact.html', {'page_title': 'Contact'})

def logout(request):
	auth.logout(request)
	return HttpResponseRedirect(reverse_lazy('static_pages:home'))
