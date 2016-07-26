from django.shortcuts import render
from .forms import RegisterForm1, RegisterForm
from django.contrib import auth
from django.http import HttpResponseRedirect
from django.contrib.auth.models import User
from .models import MyUser
# Create your views here.
def test(request): 
    return render(request,'studentforum/test.html')
	
	
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
	if request.user.is_authenticated():
		if request.method == 'POST':
			print(request.POST['change'])
			request.user.set_password(request.POST['change'])
			request.user.save()
			return HttpResponseRedirect("/home")
		else:
			return render(request, "studentforum/modify.html")
	else:
		return HttpResponseRedirect("/home")

def post_list(request):
    params = request.POST if request.method == 'POST' else None
    form = PostForm(params)
    if form.is_valid():
        post = form.save(commit = False)
        post.author = request.user
        post.save()
        form = PostForm()
    posts = Post.objects.all()
    return render(request, 'studentForum/post.html', {'posts': posts, 'form': form})

def reply_list(request, postID):
    rarams = request.POST if request.method == 'POST' else None
    form = ReplyForm(rarams)
    if form.is_valid():
        reply = form.save(commit = False)
        reply.PID = postID
        reply.save()
        form = ReplyForm()
    replies = Reply.objects.filter(PID = postID)
    posts = Post.objects.filter(id = postID)
    return render(request, 'studentForum/reply.html', {'replies': replies, 'posts': posts, 'form': form})