from django import forms
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError

from .models import User
from .utils import parse_error


class UserForm(forms.ModelForm):
	password = forms.CharField(widget=forms.PasswordInput())
	confirm_password = forms.CharField(widget=forms.PasswordInput())

	class Meta:
		model = User
		fields = ['username', 'email', 'password']

	def clean(self):
		cleaned_data = super(UserForm, self).clean()
		username = cleaned_data.get('username')
		email = cleaned_data.get('email')
		password = cleaned_data.get('password')
		confirm_password = cleaned_data.get('confirm_password')

		if password != confirm_password:
			raise forms.ValidationError('Password fields do not match.')

		user = User(username=username, email=email, password=password)

		try:
			validate_password(password, user=user)
		except ValidationError as e:
			raise forms.ValidationError(parse_error(e))
		else:
			return cleaned_data