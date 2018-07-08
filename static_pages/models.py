from django.db import models
from django.utils.safestring import mark_safe
from django.contrib.auth.models import AbstractUser
from django.urls import reverse

import hashlib


class User(AbstractUser):
    def save(self, *args, **kwargs):
        self.email = self.email.lower()
        return super(User, self).save(*args, **kwargs)

    def gravatar(self, size=60):
        digest = hashlib.md5(self.email.encode()).hexdigest()
        url = f'http://www.gravatar.com/avatar/{digest}'
        return mark_safe(f'<img src="{url}" height="{size}" width="{size}" class="gravatar">')

    def get_absolute_url(self):
    	return reverse('static_pages:profile', args=(self.pk,))