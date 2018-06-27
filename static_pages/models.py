from django.db import models
from django.utils import timezone
from django.core.validators import validate_email
from django.core.exceptions import ValidationError
from django.contrib.auth.models import AbstractUser

# class User(models.Model):
#     name = models.CharField(max_length=35, unique=True)
#     email = models.EmailField(unique=True)
#     created_at = models.DateTimeField(editable=False)
#     updated_at = models.DateTimeField()

#     def __str__(self):
#         return self.name

#     def save(self, *args, **kwargs):
#         if not self.pk:
#             self.created_at = timezone.now()

#         self.updated_at = timezone.now()
#         self.email = self.email.lower()

#         try:
#             self.full_clean()
#         except ValidationError as error:
#             raise error

#         return super(User, self).save(*args, **kwargs)


class User(AbstractUser):
    pass