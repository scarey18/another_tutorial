from django.db import models
from django.utils import timezone
from django.utils.safestring import mark_safe
from django.core.validators import validate_email
from django.core.exceptions import ValidationError
from django.contrib.auth.models import AbstractUser

import hashlib



class User(AbstractUser):
    def save(self, *args, **kwargs):
        self.email = self.email.lower()
        self.full_clean()
        return super(User, self).save(*args, **kwargs)

    def gravatar(self, size=60):
        digest = hashlib.md5(self.email.encode()).hexdigest()
        url = f'http://www.gravatar.com/avatar/{digest}'
        return mark_safe(f'<img src="{url}" height="{size}" width="{size}" class="gravatar">')