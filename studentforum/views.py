from django.shortcuts import render
from .forms import LoginForm, RegisterForm, changeForm, userForm, PasswordForm, PostForm, ReplyForm
from django.contrib import auth
from django.http import HttpResponseRedirect
from django.contrib.auth.models import User
from .models import MyUser, Post, Reply, Column, Topic
from django.core.urlresolvers import reverse
from itertools import chain
# Create your views here.
def test(request):
    posts = Post.objects.all()
    form = PostForm()
    if request.user.is_authenticated():
        if request.method == 'POST':
            params = request.POST
            form = PostForm(params)
            if form.is_valid():
                post = form.save(commit = False)
                post.author = request.user.myuser
                post.save()
                form = PostForm()
            posts = Post.objects.all()
            return render(request,'studentforum/afterLogHome.html', {'posts': posts,'form':form})
        else:
            return render(request,'studentforum/afterLogHome.html', {'posts': posts,'form':form})
    else:
        return render(request,'studentforum/home.html', {'posts': posts,'form':form})
	
	
#def login(request): 
    #params = request.POST if request.method == 'POST' else None
    #form = RegisterForm(params)
    #if form.is_valid(): 
        #user = form.save(commit=False)
        #user.save()
        #form = RegisterForm()
    #return render(request, 'studentforum/login.html', {'form': form})
	
def login(request):
    form = LoginForm()
    if request.user.is_authenticated():
        return HttpResponseRedirect("/home")
    if request.method == 'POST':
        username = request.POST.get('username', '')
        password = request.POST.get('password', '')
        user = auth.authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                auth.login(request, user)
                return HttpResponseRedirect('/home')
            else:
                return render(request, "studentforum/login.html", {'form': form})
        else:
            return render(request, "studentforum/login.html", {'form': form})
    else:
        return render(request, "studentforum/login.html", {'form': form})

def logout(request):
     auth.logout(request)
     return HttpResponseRedirect("/home")

def register(request):
    form = RegisterForm()
    if request.user.is_authenticated():
        return HttpResponseRedirect("/home")
    if request.method == 'POST':
        username = request.POST.get('username', '')
        password = request.POST.get('password', '')
        params = request.POST
        form = RegisterForm(request.POST, request.FILES)
        if form.is_valid():
            #user = form.save(commit = False)
            #user.save()
            user = User.objects.create_user(username, '', password)
            user = auth.authenticate(username=username, password=password)
            myuser = MyUser()
            if 'email' in form.cleaned_data:
            	user.email = form.cleaned_data['email']
            myuser.user = user
            if 'portrait' in form.cleaned_data:
           		myuser.portrait = form.cleaned_data['portrait']
            if 'intro' in form.cleaned_data:
           		myuser.intro = form.cleaned_data['intro']
            myuser.save()
            auth.login(request, user)
            return HttpResponseRedirect("/home")
        else:
            return render(request, "studentforum/register.html", {'form': form})
    return render(request, "studentforum/register.html", {'form': form}) 

def modifyPassword(request):
	form = PasswordForm
	if request.user.is_authenticated():
		if request.method == 'POST':
			request.user.set_password(request.POST['password'])
			request.user.save()
			return HttpResponseRedirect("/home")
		else:
			return render(request, "studentforum/modify.html",{'form': form})
	else:
		return HttpResponseRedirect("/home")

def changeInfo(request):
    if request.user.is_authenticated():
        form = changeForm()
        form1 = userForm()
        if request.method == 'POST':
            params = request.POST
            form = changeForm(request.POST,request.FILES)
            form1 = userForm(params)
            if form1.is_valid() and form.is_valid():
               print(2)
               print(request.FILES['portrait'])
               request.user.myuser.intro = request.POST['intro']
               request.user.email = request.POST['email']
               request.user.username = request.POST['username']
               if 'portrait' in request.FILES:
                    request.user.myuser.portrait = form.cleaned_data['portrait']
               request.user.myuser.save()
               request.user.save()
               form = changeForm(instance = request.user.myuser)
               form1 = userForm(instance = request.user)
        form = changeForm(instance = request.user.myuser)
        form1 = userForm(instance = request.user)
        return render(request, "studentforum/infoChange.html", {'form': form, 'form1': form1})
    else:
        return HttpResponseRedirect("/home")
		
def showDetail(request, postIDstr):
    postID = int(postIDstr)
    rarams = request.POST if request.method == 'POST' else None
    form = ReplyForm(rarams)
    post = Post.objects.get(id = postID)
    if form.is_valid() and request.user.is_authenticated():
        reply = form.save(commit = False)
        reply.PID = post
        reply.author = request.user.myuser
        reply.save()
        form = ReplyForm()
    replies = Reply.objects.filter(PID = post)
    return render(request, 'studentForum/postDetail.html', {'replies': replies, 'post': post, 'form': form})

def seekTopic(post):
    contentStr = post.content
    contentLen = len(contentStr)
    i = 0
    flag = 0
    position1 = 0
    position2 = 0
    for i in range(0, contentLen):
        if contentStr[i] == '#':
            position1 = i
            flag = 1
            break
    if flag == 0:
        return
    for i in range(position1 + 1, contentLen):
        if contentStr[i] == '#':
            position2 = i
            flag = 2
            break
    if flag == 1 or position2 == position1 + 1:
        return
    return contentStr[position1 + 1 : position2]


def showColumn(request, columnIDstr):
    columnID = int(columnIDstr)
    posts = Post.objects.filter(ofColumn = Column.objects.get(id = columnID))
    temp = Column.objects.get(id = columnID)
    temp.pstNum = posts.count()
    temp.save()
    form = PostForm()
    if request.user.is_authenticated():
        params = request.POST if request.method == 'POST' else None
        form = PostForm(params)
        if form.is_valid():
            post = form.save(commit = False)
            post.author = request.user.myuser
            post.ofColumn = Column.objects.get(id = columnID)           
            topicName = seekTopic(post)
            if topicName != None:
                if Topic.objects.filter(title = topicName).count() != 0:
                    tempTopic = Topic.objects.get(title = topicName)
                    tempTopic.pstNum += 1
                    tempTopic.save()
                    post.ofTopic = tempTopic
                else:
                    tempTopic = Topic()
                    tempTopic.title = topicName
                    tempTopic.pstNum += 1
                    tempTopic.save()
                    post.ofTopic = tempTopic
            post.save()
            form = PostForm()
        return render(request, 'studentForum/column.html', {'posts': posts, 'form': form, 'column': temp})
    else:
        return render(request, 'studentForum/column.html', {'posts': posts, 'form': form, 'column': temp})

def showTopic(request, topicIDstr):
    topicID = int(topicIDstr)
    topic = Topic.objects.get(id = topicID)
    posts = Post.objects.filter(ofTopic = topic)
    return render(request, 'studentForum/topic.html', {'posts': posts, 'topic': topic})

def directToHome(request):
	return HttpResponseRedirect("/home")

def search(request):
    key = request.GET['q']
    posts1 = Post.objects.filter(title__icontains=key)
    posts2 = Post.objects.filter(content__icontains=key)
    posts = posts1 | posts2
    if not posts:
        return render(request,'studentForum/nothingmatch.html',{})
    else:
        return render(request,'studentForum/result.html',{'posts':posts})