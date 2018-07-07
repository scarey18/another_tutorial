from django.db import models
from django.utils.safestring import mark_safe
from django.core.exceptions import ValidationError
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.password_validation import validate_password

import hashlib



class User(AbstractUser):
    def save(self, *args, **kwargs):
        self.email = self.email.lower()
        self.full_clean()
        validate_password(self.password, user=self)
        return super(User, self).save(*args, **kwargs)

    def gravatar(self, size=60):
        digest = hashlib.md5(self.email.encode()).hexdigest()
        url = f'http://www.gravatar.com/avatar/{digest}'
        return mark_safe(f'<img src="{url}" height="{size}" width="{size}" class="gravatar">')