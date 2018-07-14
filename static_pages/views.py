from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect, Http404
from django.views.generic import DetailView, CreateView, UpdateView, ListView
from django.urls import reverse, reverse_lazy
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.contrib import messages, auth
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView
from django.template.loader import render_to_string
from django.core.mail import EmailMessage

from .models import User
from .forms import UserCreateForm
from .utils import active_users


class UserProfile(LoginRequiredMixin, DetailView):
    model = User
    template_name = 'static_pages/profile.html'
    fields = ['username', 'email']

    def get_context_object_name(self, obj):
        return 'u'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = self.object.username
        return context

    def get_queryset(self):
        return active_users()


class SignupView(CreateView):
    model = User
    template_name = 'static_pages/signup.html'
    form_class = UserCreateForm

    def form_valid(self, form):
        new_user = form.save()
        pk64 = urlsafe_base64_encode(force_bytes(new_user.pk)).decode()
        activation_url = f'http://192.168.9.3:8000/activate?pk={pk64}'
        context = {'username': new_user.username, 'url': activation_url}
        email_body = render_to_string('static_pages/activation_email.html', context)
        EmailMessage('Account activation', email_body, to=[new_user.email]).send()
        return HttpResponseRedirect('activate')

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

        if auth.get_user(request) != self.object:
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

    def get_queryset(self):
        return active_users()


class LoginView(LoginView):
    template_name = 'static_pages/login.html'
    extra_context = {'page_title': 'Log in'}

    def form_valid(self, form):
        user = form.get_user()
        auth.login(self.request, user)
        next_url = self.request.POST.get('next', '')

        if self.request.POST.get('remember_me', False) is False:
            self.request.session.set_expiry(0)

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

    def get_queryset(self):
        return active_users()


def home(request):
    return render(request, 'static_pages/home.html')

def help(request):
    return render(request, 'static_pages/help.html', {'page_title': 'Help'})

def about(request):
    return render(request, 'static_pages/about.html', {'page_title': 'About'})

def contact(request):
    return render(request, 'static_pages/contact.html', {'page_title': 'Contact'})

@login_required
def logout(request):
    auth.logout(request)
    return HttpResponseRedirect(reverse_lazy('static_pages:home'))

@login_required
def deactivate(request, pk):
    user = get_object_or_404(User, pk=pk)

    if not auth.get_user(request).is_superuser:
        raise Http404
    else:
        user.is_active = False
        user.save()
        messages.success(request, "User successfully deactivated.")
        return HttpResponseRedirect(reverse_lazy('static_pages:index'))

def activate(request):
    pk64 = request.GET.get('pk', '')

    if pk64:
        pk = int(urlsafe_base64_decode(pk64).decode())
        user = get_object_or_404(User, pk=pk)
        user.is_active = True
        user.save()
        auth.login(request, user)
        messages.success(request, f"Welcome to the Sample App, {user.username}!")
        return HttpResponseRedirect(reverse('static_pages:profile', args=(user.pk,)))
    else:
        return render(request, 'static_pages/activate.html', {'page_title': 'Activate'})