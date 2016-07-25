from django.shortcuts import render
from .model import User
from dilidili_dev.models import *
from django.contrib import auth

# Create your views here.
def login(request):
    if request.user.is_authenticated():
        return HttpResponseRedirect("/home/")
    if request.method == 'POST':
        username = request.POST.get('username', '')
        password = request.POST.get('password', '')
        user = auth.authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                auth.login(request, user)
                return HttpResponseRedirect('/home/')
            else:
                return render(request, "login.html", {'error': "该用户已经被禁止登陆", 'username': username})
        else:
            return render(request, "login.html", {'error': "用户名或密码不正确", 'username': username})
    else:
        return render(request, "login.html", context=error_msg or {})

def register(request):
    if request.user.is_authenticated():
        return HttpResponseRedirect("/home/")
    if request.method == 'POST':
    	params = request.POST
    	form = RegisterForm(params)
    	if form.is_valid():
    		user = form.save(commit = False)
    		user.save()
    		form = RegisterForm()
    		auth.login(request, user)
    		return HttpResponseRedirect("/home/")
    	else:
    		return render(request, "register.html")
    return render(request, "register.html")