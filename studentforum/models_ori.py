from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone 
class MyUser(models.Model):
    user = models.OneToOneField(User, primary_key = True, default = 4)
    #sexuality = models.BooleanField(default = True)
    intro = models.TextField(max_length = 500, null = True)
    url_height = models.PositiveIntegerField(null = True)
    url_width = models.PositiveIntegerField(null = True)
    portrait = models.ImageField( upload_to = "studentforum/portraits", height_field="url_height", width_field="url_width",null = True)
    def __str__(self):
        return self.user.username
    #def __init__(self, user):
        #self.user = user
    #mid = models.AutoField(primary_key = True, unique = True)
    #another = models.CharField(max_length=100)
	
class Post(models.Model):
	id = models.AutoField(primary_key = True, unique = True)
	author = models.ForeignKey('MyUser')
	title = models.CharField(max_length = 100, verbose_name = " 标题")
	content = models.TextField(verbose_name = " 内容", null = True)
	created_at = models.DateTimeField(default = timezone.now)	
	def __str__(self):
		return self.title

class Reply(models.Model):
	id = models.AutoField(primary_key = True, unique = True)
	author = models.ForeignKey('MyUser')
	PID = models.ForeignKey('Post')
	content = models.TextField(verbose_name = " 回帖内容", null = True)
	created_at = models.DateTimeField(default = timezone.now)

	def __str__(self):
		return self.content

class Test(models.Model):
	url_height = models.PositiveIntegerField(null = True)
	url_width = models.PositiveIntegerField(null = True)
	photo = models.ImageField( upload_to = "studentforum/portraits", height_field="url_height", width_field="url_width",null = True)
	title = models.CharField(max_length = 100, default = " test")
	def __str__(self):
		return self.title
# Create your models here.

class ForWidgetTest(models.Model):
	content = models.CharField(max_length = 100, verbose_name = " 内容")
	title = models.CharField(max_length = 100, default = " test")
	def __str__(self):
		return self.title
