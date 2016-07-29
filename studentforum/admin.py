from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User

from .models import MyUser, Post, Column, Reply, Topic

# Define an inline admin descriptor for Employee model
# which acts a bit like a singleton
class MyUserInline(admin.StackedInline):
    model = MyUser
    can_delete = False
    verbose_name_plural = 'myusers'

# Define a new User admin
class UserAdmin(UserAdmin):
    inlines = (MyUserInline, )

# Re-register UserAdmin
admin.site.unregister(User)
admin.site.register(User, UserAdmin)
admin.site.register(Post)
admin.site.register(Column)
admin.site.register(Reply)
admin.site.register(Topic)
# Register your models here.
