from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect, Http404
from django.views.generic import DetailView, CreateView, UpdateView, ListView
from django.urls import reverse, reverse_lazy
from django.contrib import messages, auth
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView, PasswordResetView, PasswordResetDoneView, PasswordResetConfirmView
from django.template.loader import render_to_string
from django.core.mail import EmailMessage
from django.core.paginator import Paginator
from django.utils.crypto import get_random_string

from .models import User, Micropost
from .forms import UserCreateForm, UserUpdateForm, MicropostForm
from .utils import active_users


class UserProfile(LoginRequiredMixin, DetailView):
    model = User
    template_name = 'static_pages/profile.html'
    fields = ['username', 'email']

    def get_context_object_name(self, obj):
        return 'u'

    def get_context_data(self, **kwargs):
        page_num = self.request.GET.get('page', 1)
        posts = self.object.microposts()

        context = super().get_context_data(**kwargs)
        context['page_title'] = self.object.username
        context['page_obj'] = Paginator(posts, 10).page(page_num)
        context['posts'] = posts
        return context

    def get_queryset(self):
        return active_users()


class SignupView(CreateView):
    model = User
    template_name = 'static_pages/signup.html'
    form_class = UserCreateForm

    def form_valid(self, form):
        new_user = form.save()
        activation_id = get_random_string(length=32)
        new_user.activation_id = activation_id
        new_user.save()
        activation_url = f'http://192.168.9.3:8000/activate?id={activation_id}'
        context = {'username': new_user.username, 'url': activation_url}
        email_body = render_to_string('static_pages/activation_email.html', context)
        EmailMessage('Account activation', email_body, to=[new_user.email]).send()
        return HttpResponseRedirect(reverse_lazy('static_pages:activate'))

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = 'Sign up'
        return context


class EditUser(LoginRequiredMixin, UpdateView):
    model = User
    template_name = 'static_pages/edit_user.html'
    form_class = UserUpdateForm

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


class PasswordReset(PasswordResetView):
    template_name = 'static_pages/password_reset.html'
    success_url = reverse_lazy('static_pages:password_reset_done')
    extra_context = {'page_title': 'Password reset'}
    email_template_name = 'static_pages/password_reset_email.html'
    subject_template_name = 'static_pages/password_reset_subject.txt'


class PasswordResetDone(PasswordResetView):
    template_name = 'static_pages/password_reset_done.html'
    extra_context = {'page_title': 'Email sent'}


class PasswordResetConfirm(PasswordResetConfirmView):
    template_name = 'static_pages/password_reset_confirm.html'
    extra_context = {'page_title': 'Change password'}

    def form_valid(self, form):
        form.save()
        auth.logout(self.request)
        messages.success(self.request, "Your password has been reset. Please login with the new password to continue.")
        return HttpResponseRedirect(reverse_lazy('static_pages:login'))


def home(request):
    page_num = request.GET.get('page', 1)
    user = auth.get_user(request)
    context = {
        'form': MicropostForm(),
        'page_obj': Paginator(user.microposts(), 10).page(page_num),
    } if user.is_authenticated else None
    return render(request, 'static_pages/home.html', context)

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
    activation_id = request.GET.get('id', '')

    if activation_id:
        user = get_object_or_404(User, activation_id=activation_id)

        if user.is_active:
            return HttpResponseRedirect(reverse_lazy('static_pages:home'))

        user.is_active = True
        user.activation_id = None
        user.save()
        messages.success(request, f"Your account has been successfully activated, {user.username}! Please log in to continue.")
        return HttpResponseRedirect(reverse('static_pages:profile', args=(user.pk,)))

    else:
        return render(request, 'static_pages/activate.html', {'page_title': 'Activate'})

@login_required
def create_micropost(request):
    if request.method == 'POST':
        form = MicropostForm(request.POST)

        if form.is_valid():
            content = form.cleaned_data['content']
            user = auth.get_user(request)
            Micropost.objects.create(content=content, user=user)
            messages.success(request, "Successfully posted!")
        else:
            messages.error(request, "Unable to post.")

        return HttpResponseRedirect(reverse_lazy('static_pages:home'))

    else:
        raise Http404