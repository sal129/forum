from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone 
class MyUser(models.Model):
    user = models.OneToOneField(User, primary_key = True, default = 4)
    isdeleted=models.BooleanField(default=False)
    isforbidden=models.BooleanField(default=False)
    #sexuality = models.BooleanField(default = True)
    intro = models.TextField(max_length = 500, null = True)
    url_height = models.PositiveIntegerField(null = True)
    url_width = models.PositiveIntegerField(null = True)
    portrait = models.ImageField( upload_to = "studentforum/portraits", height_field="url_height", width_field="url_width",null = True)
    manageType = models.IntegerField(default = 0)#0: 普通用户    1：column管理员   2：总管理员
    score = models.IntegerField(default = 0)
    age = models.IntegerField(default = 0)
    followNum = models.IntegerField(default = 0)
    follow = models.ManyToManyField('MyUser', symmetrical = False)
    fansNum = models.IntegerField(default = 0)
    pstNum = models.IntegerField(default = 0)
    collectPstNum = models.IntegerField(default = 0)
    collectPst = models.ManyToManyField('Post')
    likePst = models.ManyToManyField('Post',related_name = "likepersons")
    likeRst = models.ManyToManyField('Reply',related_name = "likepersonlist")
    reportPst = models.ManyToManyField('Post',related_name = "reportposts")
    reportRst = models.ManyToManyField('Reply',related_name = "reportreplies")
    reportRpytoRpy = models.ManyToManyField('ReplytoReply',related_name = "reportreptorep")
    collectClsNum = models.IntegerField(default = 0)
    collectCls = models.ManyToManyField('Column')
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
	content = models.TextField(verbose_name = " 内容（内容中插入#相关话题#可以将贴子与话题关联起来）", null = True)
	created_at = models.DateTimeField(default = timezone.now)
	latestupdate = models.DateTimeField(default = timezone.now)
	url_height = models.PositiveIntegerField(null = True)
	url_width = models.PositiveIntegerField(null = True)
	attachment = models.FileField( upload_to = "studentforum/attachments",null = True)
	photo = models.ImageField( upload_to = "studentforum/photos", height_field="url_height", width_field="url_width",null = True)
	ofColumn = models.ForeignKey('Column', null = True)
	ofTopic = models.ForeignKey('Topic', null = True)
	supportNum = models.IntegerField(default = 0)
	reportNum = models.IntegerField(default = 0)
	collectNum = models.IntegerField(default = 0)
	ischecked = models.BooleanField(default = False)
	isreported = models.BooleanField(default = False)
	def __str__(self):
		return self.title

class Reply(models.Model):
	id = models.AutoField(primary_key = True, unique = True)
	author = models.ForeignKey('MyUser')
	PID = models.ForeignKey('Post')
	content = models.TextField(verbose_name = " 回帖内容", null = True)
	created_at = models.DateTimeField(default = timezone.now)
	url_height = models.PositiveIntegerField(null = True)
	url_width = models.PositiveIntegerField(null = True)
	attachment = models.FileField( upload_to = "studentforum/attachments",null = True)
	photo = models.ImageField( upload_to = "studentforum/photos", height_field="url_height", width_field="url_width",null = True)
	supportNum = models.IntegerField(default = 0)
	reportNum = models.IntegerField(default = 0)
	ischecked = models.BooleanField(default = False)
	isreported = models.BooleanField(default = False)
	def __str__(self):
		return self.content

class Column(models.Model):
	id = models.AutoField(primary_key = True, unique = True)
	name = models.CharField(max_length = 20, unique = True)
	pstNum = models.IntegerField(default = 0)
	collectNum = models.IntegerField(default = 0)
	manager = models.ManyToManyField('MyUser')
	def __str__(self):
		return self.name

class Topic(models.Model):
	id = models.AutoField(primary_key = True, unique = True)
	topicType = models.IntegerField(default = 0)
	title = models.CharField(max_length = 100, unique = True)
	pstNum = models.IntegerField(default = 0) 
	heat = models.IntegerField(default = 0)
	def __str__(self):
		return self.title
 
class Letter(models.Model):
	id = models.AutoField(primary_key = True, unique = True)
	userFrom = models.ForeignKey('MyUser', related_name = 'reverse_from', null = True)
	userTo = models.ForeignKey('MyUser', related_name = 'reverse_to', null = True)
	content = models.TextField(max_length = 20, verbose_name = "内容")
	created_at = models.DateTimeField(default = timezone.now)


class ReplytoReply(models.Model):
    id=models.AutoField(primary_key=True,unique=True)
    author=models.ForeignKey('MyUser')
    PID=models.ForeignKey('Reply')
    content=models.TextField(verbose_name="楼中楼回帖",null=True)
    created_at=models.DateTimeField(default = timezone.now)
    
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

class PostTotal(models.Model):
	id=models.AutoField(primary_key=True,unique=True)
	forpost = models.OneToOneField(Post, null = True)
	forreply = models.OneToOneField(Reply, null = True)
	forreplytoreply = models.OneToOneField(ReplytoReply, null = True)
	type1 = models.PositiveIntegerField(null = True)
	firstReportTime = models.DateTimeField(default = timezone.now)
	reportNum = models.PositiveIntegerField(default = 0)
	publishTime = models.DateTimeField(default = timezone.now)
	ischecked = models.BooleanField(default = False)
	def __str__(self):
		if self.type1 == 0:
			return self.forpost.__str__()
		elif self.type1 == 1:
			return self.forreply.__str__()
		elif self.type1 == 2:
			return self.forreplytoreply.__str__()

class ForWidgetTest(models.Model):
	content = models.CharField(max_length = 100, verbose_name = " 内容")
	title = models.CharField(max_length = 100, default = " test")
	def __str__(self):
		return self.title

class TestFile(models.Model):
	file= models.FileField( upload_to = "studentforum/files",null = True)
	title = models.CharField(max_length = 100, default = " test")
	def __str__(self):
		return self.file.__str__()

