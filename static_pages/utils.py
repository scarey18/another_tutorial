

from .models import User

def active_users():
	return User.objects.filter(is_active=True)