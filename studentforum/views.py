from django.shortcuts import render
from django.shortcuts import render_to_response
from .forms import RegisterForm1, RegisterForm, changeForm, userForm, PasswordForm, PostForm, ReplyForm,ReplytoReplyForm
from django.contrib import auth
from django.http import HttpResponseRedirect
from django.contrib.auth.models import User
from .models import MyUser, Post, Reply,ReplytoReply
from django.core.urlresolvers import reverse
from django.views.decorators.csrf import csrf_exempt
from django import template
from django.views.decorators.csrf import ensure_csrf_cookie
from django.http import HttpResponseRedirect, HttpResponse
import json
#=template.Library()
#@register.simple_tag
#def reprep_tag(obj):
 #   return ReplytoReply.objects.filter(PID=reply)
#register.simple_tag(reprep_tag)
# Create your views here.
switch=False

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
    
        
    usergroup=MyUser.objects.all()
    for u in usergroup:
        print(u.isdeleted)
    if request.user.is_authenticated():
        print("request.user is {0}".format(request.user.myuser.isdeleted))
        if request.user.isdeleted==False:
            return HttpResponseRedirect("/home")
        else:
            return render(request, "studentforum/nothingmatch.html", {'form': form}) 
    if request.method == 'POST':
        username = request.POST.get('username', '')
        usergroup=MyUser.objects.all()
        check=False
        for u in usergroup:
            print(u.isdeleted)
            if u.user.username==username and u.isdeleted==True:
                check=True
        if check==True:
            return render(request, "studentforum/login.html", {'form': form})
        password = request.POST.get('password', '')
        user = auth.authenticate(username=username, password=password)
        if user is not None :
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
		


def directToHome(request):
	return HttpResponseRedirect("/home")


def search(request):
    key = request.GET['q']
    
    posts=Post.objects.filter(title__icontains=key)
    if not posts:
        return render(request,'studentForum/nothingmatch.html',{})
    else:
        return render(request,'studentForum/result.html',{'posts':posts})
@ensure_csrf_cookie
def showDetail(request, postIDstr):
    print(request.is_ajax())
    if request.is_ajax() and request.user.is_authenticated():
        req = json.loads(request.POST["data"])
        reptorep1 = ReplytoReply()
        reptorep1.author = request.user.myuser
        reptorep1.content = req["content"]
        reptorep1.PID = Reply.objects.get(id = int(req["replyid"]))
        reptorep1.save()
        return HttpResponse(json.dumps({"content":reptorep1.content,"author":reptorep1.author.user.username}))
    global switch
    switch=False
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
    isfavor=False
    #print(request.user.myuser.collectPst)
    #print(request.user.myuser.collectPstNum)
    if request.user.is_authenticated():
        if request.user.myuser.collectPst.filter(id=post.id).exists():
            print("IT EXSITS!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
            print(post.content)
            print("isfavor is {0}".format(isfavor))
            isfavor=True
        
    else:
        print("there is no such post!!!!!!!!!!!!!!")
    print("now isfavor is {0}".format(isfavor))
    return render(request, 'studentForum/postDetail.html', {'replies': replies, 'post': post, 'form': form,'isfavor':isfavor})



@ensure_csrf_cookie
def countgood(request):
    
    if request.is_ajax and request.user.is_authenticated():
        req=json.loads(request.POST["data"])
        reply=Reply()
        reply=Reply.objects.get(id=int(req["replyid"]))
        tmp=reply.supportNum+1
        reply.supportNum=tmp
        print(reply.supportNum)
        #reply.numgood++
        reply.save()
        return HttpResponse(json.dumps({"num":reply.supportNum,"whatever":"whatever"}))

    
@ensure_csrf_cookie
def postcountgood(request,w,h,atever):
    if request.is_ajax and request.user.is_authenticated():
        req=json.loads(request.POST["data"])
        print(req["postid"])
        post=Post.objects.get(id=int(req["postid"]))
        tmp=post.supportNum+1
        post.supportNum=tmp
        #print(post.supportNum)
        post.save()
        return HttpResponse(json.dumps({"num":post.supportNum,"whatever":"whatever"}))
        
@ensure_csrf_cookie
def postfavor(request,w,h,a,tever):
    if request.is_ajax and request.user.is_authenticated():
        #global req
        req=json.loads(request.POST["data"])
        #print(request.user.myuser.id)
        print(req["target"])
        #print(typeof(req["target"]))
        #st=
        if str(req["target"]) == "include":
            req=json.loads(request.POST["data"])
            print("this is include")
            post=Post.objects.get(id=int(req["postid"]))
            user=request.user.myuser
            user.collectPst.add(post)
            tmp=user.collectPstNum+1
            user.collectPstNum=tmp
            print(user.collectPstNum)
            user.save()
            post.save()
            print("this is include")
            return HttpResponse(json.dumps({"num":user.collectPstNum,"message":"已收藏，点击取消收藏"}))
        if str(req["target"]) == "exclude":
            #global req
            req=json.loads(request.POST["data"])
            post=Post.objects.get(id=int(req["postid"]))
            user=request.user.myuser
            user.collectPst.remove(post)
            tmp=user.collectPstNum-1
            user.collectPstNum=tmp
            user.save()
            return HttpResponse(json.dumps({"num":user.collectPstNum,"message":"收藏该贴"}))


    
        #user
        
def replytoreply(request,replyIDstr,postIDstr):
    postID=int(postIDstr)
    replyID=int(replyIDstr)
    para=request.POST if request.method=='POST' else None
    form=ReplytoReplyForm(para)
    reply=Reply.objects.get(id=replyID)
    if form.is_valid() and request.user.is_authenticated():
        replytoreply=form.save(commit=False)
        replytoreply.PID=reply
        replytoreply.author=request.user.myuser
        replytoreply.save()
        form=ReplytoReplyForm()
    replytoreplies=ReplytoReply.objects.filter(PID=reply)
    post=Post.objects.get(id=postID)
   
    return render(request,'studentForum/replyDetail.html',{'replytoreplies':replytoreplies,'reply':reply,'reprepform':form,'post':post})
def deluser(request,uid):
    user=MyUser.objects.get(user_id=uid)
    
    user.isdeleted=True
    user.save()
    usergroup=MyUser.objects.all()
    print('whatthehell')
    print(user.isdeleted)
    for u in usergroup:
        print(u.user_id)
        print(u.isdeleted)
    return render(request,'studentForum/userinfo.html',{'usergroup':usergroup})
    
def reptorep(request,replyIDstr,postIDstr):
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
    replyid=int(replyIDstr)
    reply_=Reply.objects.get(id=replyid)
    reprep=ReplytoReply.objects.filter(PID=reply_)
    global switch
    if switch:
        switch=False
    elif not switch:
        switch=True
    
    #reply_.showrr=!reply_.showrr
    print(reprep)
    print(reply_.showrr)
    return render(request,'studentForum/postDetail.html',{'reprep':reprep,'replies': replies, 'post': post, 'form': form,'switch':switch, 'replyId':replyid})


###删除账号
def delete_account(request):
    usergroup=MyUser.objects.all()
    #for user in usergroup:
        #print(user.user.id)
    # user=MyUser.objects.get(user_id=1)
    return render(request,'studentForum/userinfo.html',{'usergroup':usergroup})
    #return render(request,'studentForum/usermanage.html',{'user':user})
    #user=MyUser.user.filter(id=userid)
    #print 
