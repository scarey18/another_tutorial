from django.db import models
from django.urls import reverse
from django.utils import timezone
from django.utils.safestring import mark_safe
from django.contrib.auth.models import AbstractUser
from django.core.paginator import Paginator

import hashlib


class User(AbstractUser):
    is_active = models.BooleanField(default=False)
    activation_id = models.SlugField(null=True, blank=True, default=None)

    REQUIRED_FIELDS = ['email']

    def __str__(self):
        return self.username

    def gravatar(self, size=80):
        digest = hashlib.md5(self.email.encode()).hexdigest()
        url = f'http://www.gravatar.com/avatar/{digest}'
        return mark_safe(f'<img src="{url}" height="{size}" width="{size}" class="gravatar">')

    def index_gravatar(self):
        return self.gravatar(50)

    def get_absolute_url(self):
        return reverse('static_pages:profile', args=(self.pk,))

    def microposts(self):
        return self.micropost_set.all().order_by('-created_at')

    def feed_page_obj(self, request):
        page_num = request.GET.get('page', 1)
        return Paginator(self.microposts(), 10).page(page_num)


class Micropost(models.Model):
    content = models.TextField(max_length=140)
    created_at = models.DateTimeField(editable=False)
    updated_at = models.DateTimeField()
    user = models.ForeignKey(User, on_delete=models.CASCADE, editable=False)

    def __str__(self):
        content = self.content.split(' ')
        abbrv = ' '.join(content[:10]) + '...' if len(content) > 10\
            else ' '.join(content)
        return abbrv if len(abbrv) < 40 else abbrv[:40] + '...'

    def save(self, *args, **kwargs):
        if not self.pk:
            self.created_at = timezone.now()
        self.updated_at = timezone.now()
        return super().save(*args, **kwargs)
