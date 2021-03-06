from django.db import models
from django.urls import reverse
from django.utils import timezone
from django.utils.safestring import mark_safe
from django.contrib.auth.models import AbstractUser

import hashlib



class User(AbstractUser):
    is_active = models.BooleanField(default=False)
    activation_id = models.SlugField(null=True, blank=True, default=None)
    following = models.ManyToManyField(
                    'self',
                    symmetrical=False,
                    related_name='followers',
                    blank=True,
                    default=None
                )

    REQUIRED_FIELDS = ['email']

    def __str__(self):
        return self.username

    def get_absolute_url(self):
        return reverse('static_pages:profile', args=(self.pk,))

    def gravatar(self, size=80):
        digest = hashlib.md5(self.email.encode()).hexdigest()
        url = f'http://www.gravatar.com/avatar/{digest}'
        img_tag = f'<img src="{url}" height="{size}" width="{size}" class="gravatar">'
        wrapped_img_tag = f'<a href="{self.get_absolute_url()}">{img_tag}</a>'
        return mark_safe(wrapped_img_tag)

    def index_gravatar(self):
        return self.gravatar(50)

    def following_gravatar(self):
        return self.gravatar(30)

    def microposts(self):
        return self.micropost_set.all().order_by('-created_at')

    def active_following(self):
        return self.following.filter(is_active=True)

    def active_followers(self):
        return self.followers.filter(is_active=True)

    def feed(self):
        return Micropost.objects.filter(
            models.Q(user__in=self.active_following()) |
            models.Q(user=self)
        ).order_by('-created_at')


def image_file_path(post, filename):
    return f'micropost_pictures/user_{post.user.pk}/{filename}'

class Micropost(models.Model):
    content = models.TextField(max_length=140)
    created_at = models.DateTimeField(editable=False)
    updated_at = models.DateTimeField()
    user = models.ForeignKey(User, on_delete=models.CASCADE, editable=False)
    picture = models.ImageField(upload_to=image_file_path, blank=True, null=True)

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

    def resized_pic_width(self, size=400):
        return size if self.picture.width >= size else self.picture.width