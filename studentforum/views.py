from django.shortcuts import render
from django.shortcuts import render_to_response
from .forms import RegisterForm1, RegisterForm, changeForm, userForm, PasswordForm, PostForm, ReplyForm
from django.contrib import auth
from django.http import HttpResponseRedirect
from django.contrib.auth.models import User
from .models import MyUser, Post, Reply
from django.core.urlresolvers import reverse
from django.views.decorators.csrf import csrf_exempt
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
            print(posts)
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
    form = RegisterForm1()
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
        form = RegisterForm(params)
        if form.is_valid():
            #user = form.save(commit = False)
            #user.save()
            form = RegisterForm()
            user = User.objects.create_user(username, '', password)
            user = auth.authenticate(username=username, password=password)
            myuser = MyUser()
            myuser.user = user
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
	    if request.method == 'POST':
	        request.user.myuser.intro = request.POST['intro']
	        request.user.email = request.POST['email']
	        request.user.username = request.POST['username']
	        request.user.myuser.save()
	        request.user.save()
	        form = changeForm(instance = request.user.myuser)
	        form1 = userForm(instance = request.user)
	        return render(request, "studentforum/infoChange.html", {'form': form, 'form1': form1})
	    else:
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

def directToHome(request):
	return HttpResponseRedirect("/home")


def search(request):
    key = request.GET['q']
    posts=Post.objects.filter(title__icontains=key)
    if not posts:
        return render(request,'studentForum/nothingmatch.html',{})
    else:
        return render(request,'studentForum/result.html',{'posts':posts})
    
    #if not key :
    #    message = u'请输入搜索内容'
#        return render_to_response('studentForum/result.html',{'message':message})
 
    #else :
     #message = u'你输入的是' + key
        #return render_to_response('studentForum/result.html',{'message':message})
#def trysearch(request):   
 #   data='abc'
#data=request.GET['searchbox']
   # return render(request,'studentForum/try.html',{'try':data})