from django.db import models
from django.utils import timezone
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser

# Create your models here.
class User(AbstractBaseUser):
	id = models.AutoField(primary_key = True, unique = True)
    username = models.CharField(max_length = 30, unique=True)
    name = models.CharField(max_length = 30, unique=True)
    email = models.EmailField(max_length = 100, unique=True)
    sexuality = models.BooleanField(default = True)
    intro = model.TextField(max_length = 500)

class Post(models.Model):
	author = models.ForeignKey('auth.User')
	title = models.CharField(max_length = 100, verbose_name = " 标题")
	content = models.TextField(verbose_name = " 内容")
	created_at = models.DateTimeField(default = timezone.now)
	
	def __str__(self):
		return self.title