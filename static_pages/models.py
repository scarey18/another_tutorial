from django.db import models
from django.urls import reverse
from django.utils.safestring import mark_safe
from django.contrib.auth.models import AbstractUser

import hashlib


class User(AbstractUser):
    is_active = models.BooleanField(default=False)

    REQUIRED_FIELDS = ['email']

    def gravatar(self, size=60):
        digest = hashlib.md5(self.email.encode()).hexdigest()
        url = f'http://www.gravatar.com/avatar/{digest}'
        return mark_safe(f'<img src="{url}" height="{size}" width="{size}" class="gravatar">')

    def index_gravatar(self):
        return self.gravatar(50)

    def get_absolute_url(self):
        return reverse('static_pages:profile', args=(self.pk,))