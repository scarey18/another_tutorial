from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect, Http404
from django.views.generic import DetailView, CreateView, UpdateView, ListView
from django.urls import reverse, reverse_lazy
from django.contrib import messages, auth
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView
from django.contrib.auth.models import AnonymousUser

from .models import User
from .forms import UserCreateForm

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
    form_class = UserCreateForm

    def form_valid(self, form):
        new_user = form.save()
        auth.login(self.request, new_user)
        self.request.session.set_expiry(0)
        message = f"Welcome to the Sample App, {new_user.username}!"
        messages.success(self.request, message)
        return HttpResponseRedirect(new_user.get_absolute_url())

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = 'Sign up'
        return context


class EditUser(LoginRequiredMixin, UpdateView):
    model = User
    template_name = 'static_pages/edit_user.html'
    form_class = UserCreateForm

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        current_user = auth.get_user(request)

        if current_user != self.object:
            return HttpResponseRedirect(reverse('static_pages:profile', args=(current_user.pk,)))
        else:
            return super().get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        current_user = auth.get_user(request)

        if current_user != self.object:
            raise Http404
        else:
            return super().post(request, *args, **kwargs)

    def form_valid(self, form):
        user = form.save()
        auth.login(self.request, user)
        messages.success(self.request, "Profile successfully updated!")
        return HttpResponseRedirect(user.get_absolute_url())

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = 'Edit'
        return context


class LoginView(LoginView):
    template_name = 'static_pages/login.html'
    extra_context = {'page_title': 'Log in'}

    def form_valid(self, form):
        user = form.get_user()
        auth.login(self.request, user)

        if self.request.POST.get('remember_me', False) is False:
            self.request.session.set_expiry(0)

        next_url = self.request.POST.get('next', '')
        return HttpResponseRedirect(next_url) if next_url\
            else HttpResponseRedirect(reverse_lazy('static_pages:home'))


class IndexView(LoginRequiredMixin, ListView):
    template_name = 'static_pages/index.html'
    model = User
    paginate_by = 10

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = 'Users'
        return context


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
