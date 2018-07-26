from django import forms
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.forms import UserCreationForm, UserChangeForm

from .models import User, Micropost


class UserCreateForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for fieldname in ['username', 'password2']:
            self.fields[fieldname].help_text = None
        self.fields['email'].required = True


class UserUpdateForm(UserChangeForm):
    class Meta:
        model = User
        fields = ['username', 'email']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].help_text = None
        del self.fields['password']


class MicropostForm(forms.ModelForm):
    class Meta:
        model = Micropost
        fields = ['content', 'picture']
        labels = {'content': _(''), 'picture': _('Add an image:')}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['content'].widget.attrs['placeholder'] = 'Compose new post...'