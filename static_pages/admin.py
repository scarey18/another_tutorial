from django.contrib import admin

from .models import User, Micropost

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
	exclude = ('groups',)

@admin.register(Micropost)
class MicropostAdmin(admin.ModelAdmin):
	pass