
from django.shortcuts import render, render_to_response
from .forms import LoginForm, RegisterForm, changeForm, userForm, PasswordForm, PostForm, ReplyForm, TestForm,TestWidgetForm, TestFileForm
from django.contrib import auth
from django.http import HttpResponseRedirect, HttpResponse, StreamingHttpResponse
from django.contrib.auth.models import User
from .models import MyUser, Post, Reply, TestFile, ReplytoReply,PostTotal
from django.core.urlresolvers import reverse
from django.views.decorators.csrf import ensure_csrf_cookie
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
from django.utils import timezone 
import os
import json
import codecs
# Create your views here.
def test(request):
    posts = Post.objects.order_by('-latestupdate')
    print("start1")
    form = PostForm()
    print("start2")
    if request.user.is_authenticated():
        if request.method == 'POST':
            print(1)
            params = request.POST
            form = PostForm(request.POST, request.FILES)
            if form.is_valid():
                print(2)
                post = form.save(commit = False)
                post.author = request.user.myuser
                post.save()
                fortotal = PostTotal()
                fortotal.type1 = 0
                fortotal.forpost = post
                fortotal.save()
                print(post.photo)
                form = PostForm()
            posts = Post.objects.order_by('-latestupdate')
            return render(request,'studentforum/afterLogHome.html', {'posts': posts,'form':form})
        else:
            return render(request,'studentforum/afterLogHome.html', {'posts': posts,'form':form})
    else:
        print("start3")
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


def big_file_download(request,filename):
    def file_iterator(filenamet, chunk_size=512):
        print(2)
        with open(filenamet, "rb") as f:
            print("open")
            while True:
                c = f.read(chunk_size)
                if c:
                    yield c
                else:
                    break
    response = StreamingHttpResponse(file_iterator(filename))
    filename1 = filename[filename.rindex("/")+1:]
    clientSystem = request.META['HTTP_USER_AGENT']
    if clientSystem.find('Windows') > -1:
        print(2.5)
        filename1 = filename1.encode().decode('ISO8859-1')
    else:
        print(2.6)
        filename1 = filename1.encode().decode('utf-8')
    print(filename1)
    print(3)
    response['Content-Type'] = 'application/octet-stream'
    response['Content-Disposition'] = 'attachment;filename= %s' %filename1
    print(4)
    return response

def downloadpost(request,postIDstr):
    the_file_name = Post.objects.all().get(id = postIDstr).attachment.__str__()
    the_file_name=os.path.join(settings.MEDIA_ROOT,the_file_name)
    return big_file_download(request,the_file_name)

def downloadreply(request,replyIDstr):
    print("startreplydownload")
    the_file_name = Reply.objects.all().get(id = replyIDstr).attachment.__str__()
    the_file_name=os.path.join(settings.MEDIA_ROOT,the_file_name)
    return big_file_download(request,the_file_name)

@ensure_csrf_cookie		
def showDetail(request, postIDstr):

    post = Post.objects.get(id = int(postIDstr))
    if request.is_ajax() and request.user.is_authenticated():
        req = json.loads(request.POST["data"])
        if req["type"] == "reply":
            reptorep1 = ReplytoReply()
            reptorep1.author = request.user.myuser
            reptorep1.content = req["content"]
            reptorep1.PID = Reply.objects.get(id = int(req["replyid"]))
            reptorep1.save()
            post.latestupdate = reptorep1.created_at
            post.save()
            fortotal = PostTotal()
            fortotal.type1 = 2
            fortotal.forpost = reptorep1
            fortotal.save()
            return HttpResponse(json.dumps({"content":reptorep1.content,"author":reptorep1.author.user.username}))
        elif req["type"] == "reportpost":
            tempt = Post.objects.get(id = int(req["postid"])).posttotal
            tempt.type = 0
            if tempt.reportNum == 0:
                tempt.firstReportTime = timezone.now
                tempt.reportNum = 1
            else:
                tempt.reportNum = tempt.reportNum + 1
            tempt.save()


            return HttpResponse(json.dumps({"content":""}))

    postID = int(postIDstr)
    rarams = request.POST if request.method == 'POST' else None
    form = ReplyForm(request.POST, request.FILES)
    post = Post.objects.get(id = postID)
    postfilename = post.attachment.__str__()
    if postfilename:
        postfilename = postfilename[postfilename.rindex("/")+1:]
    else:
        postfilename  = ""
    replies = Reply.objects.filter(PID = post)

    if request.method == 'POST':
        if 'content' in request.POST:
            print("hascontent")
            form = ReplyForm(request.POST, request.FILES)
            if form.is_valid() and request.user.is_authenticated():
                print("valid")
                reply = form.save(commit = False)
                reply.PID = post
                reply.author = request.user.myuser
                reply.save()
                form = ReplyForm()
                post.latestupdate = reply.created_at
                post.save()
                fortotal = PostTotal()
                fortotal.type1 = 1
                fortotal.forpost = reply
                fortotal.save()



    replylist = []
    for reply in replies:
        if reply.author == post.author:
            belongToAuthor = "True"
        else:
            belongToAuthor = "False"
        replyfilename = reply.attachment.__str__()
        if replyfilename:
            replyfilename = replyfilename[replyfilename.rindex("/")+1:]
        else:
            replyfilename = ""
        replylist.append({"reply1": reply,"replyfilename":replyfilename, "belongToAuthor":belongToAuthor})
    return render(request, 'studentForum/postDetail.html', {'replies': replies, 'post': post, 'postfilename':postfilename,'form': form,'replylist': replylist,})

def directToHome(request):
	return HttpResponseRedirect("/home")

def testfile(request):
    form = TestFileForm()
    if request.method == 'POST':
        rarams = request.POST
        form = TestFileForm(request.POST,request.FILES)
        print(1)
        if form.is_valid():
            print(2)
            file = form.save(commit = True)
            form = TestFileForm(instance = file)
            filepath = file.file.__str__()
            print(filepath[filepath.rindex("/")+1:])
            #return render(request, 'studentForum/showphoto.html',{'photo':photo})
    return render(request, 'studentForum/testphoto.html', {'form': form})

def showphoto(request):
    return render(request, 'studentForum/showphoto.html')

def search(request):
    key = request.GET['q']
    posts=Post.objects.filter(title__icontains=key)
    if not posts:
        return render(request,'studentForum/nothingmatch.html',{})
    else:
        return render(request,'studentForum/result.html',{'posts':posts})

def showWidget(request):
    form = TestWidgetForm()
    return render(request, 'studentForum/testWidget.html', {'form': form})

@ensure_csrf_cookie
def testajax(request):
	if request.method == 'POST':
		print(request.POST)
		req = json.loads(request.POST["data"])
		print(req[0]["name"])
		print(1)
		#HttpResponseRedirect("/home")
		#return render(request,'studentForum/ajax_submit.html')
		return  HttpResponse(json.dumps({"content":"nihao"}))
	print(2)
	return render(request, 'studentForum/ajax.html')

def testajax2(request):
	print(request.POST)
	return HttpResponse(json.dumps({"content":"nihao"}))

def showfile(request):
     def big_file_download(request):
         def file_iterator(file_name, chunk_size=512):
             print(2)
             with open(file_name, "rb") as f:
                 print("open")
                 while True:
                     c = f.read(chunk_size)
                     if c:
                         yield c
                     else:
                         break
         # path=os.path.join(settings.MEDIA_ROOT,'upload')
         # print(path)
         the_file_name = "/vagrant/forum/test/res/studentforum/files/try4.zip"
         #the_file_name = TestFile.objects.all().get(id = 11).__str__()
         #the_file_name=os.path.join(settings.MEDIA_ROOT,the_file_name)
         print(the_file_name)
         filename = the_file_name[the_file_name.rindex("/")+1:]
         #filename = str(filename.decode("unicode").encode("utf-8"))
         #filename = filename.encode("unicode")
         #filename = str(codecs.decode(filename, 'utf-8'))
         print(filename)
         clientSystem = request.META['HTTP_USER_AGENT']
         if clientSystem.find('Windows') > -1:
             filename = filename.encode().decode('ISO8859-1')
         else:
             filename = filename.encode().decode('utf-8')
         print(filename)
         #print(filename.encode('ascii'))
         response = StreamingHttpResponse(file_iterator(the_file_name))
         response['Content-Type'] = 'application/octet-stream'
         #response.setHeader("Content-Disposition", "attachment; filename=" + fileName);
         #fileName = new String(as.getBytes("GB2312"), "ISO_8859_1"); 
         response['Content-Disposition'] = 'attachment;filename= %s' %filename
         print('attachment;filename='+filename)
         print(1)
         return response
     if request.method == 'POST':
        return big_file_download(request)
     else:
        return render(request, 'studentForum/showfile.html')


@ensure_csrf_cookie
def countgood(request):
    
    if request.is_ajax and request.user.is_authenticated():
        req=json.loads(request.POST["data"])
        reply=Reply()
        reply=Reply.objects.get(id=int(req["replyid"]))
        if not request.user.myuser in reply.likepersonlist.all():
            tmp=reply.supportNum + 1
            request.user.myuser.likeRst.add(reply)
        else:
            tmp=reply.supportNum
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
        if not request.user.myuser in post.likepersons.all():
            tmp=post.supportNum+1
            request.user.myuser.likePst.add(post)
        else:
            tmp=post.spportNum
        post.supportNum=tmp
        #print(post.supportNum)
        post.save()
        return HttpResponse(json.dumps({"num":post.supportNum,"whatever":"whatever"}))


def testdownload(request):
     print("downloadstart")
     def big_file_download(request):
         def file_iterator(file_name, chunk_size=512):
             print(2)
             with open(file_name, "rb") as f:
                 print("open")
                 while True:
                     c = f.read(chunk_size)
                     if c:
                         yield c
                     else:
                         break
         # path=os.path.join(settings.MEDIA_ROOT,'upload')
         # print(path)
         the_file_name = "/vagrant/forum/test/res/studentforum/files/新建文本文档.txt"
         #the_file_name = TestFile.objects.all().get(id = 11).__str__()
         #the_file_name=os.path.join(settings.MEDIA_ROOT,the_file_name)
         print(the_file_name)
         filename = the_file_name[the_file_name.rindex("/")+1:]
         #filename = str(filename.decode("unicode").encode("utf-8"))
         #filename = filename.encode("unicode")
         #filename = str(codecs.decode(filename, 'utf-8'))
         print(filename)
         clientSystem = request.META['HTTP_USER_AGENT']
         if clientSystem.find('Windows') > -1:
             filename = filename.encode().decode('ISO8859-1')
         else:
             filename = filename.encode().decode('utf-8')
         print(filename)
         #print(filename.encode('ascii'))
         response = StreamingHttpResponse(file_iterator(the_file_name))
         response['Content-Type'] = 'application/octet-stream'
         #response.setHeader("Content-Disposition", "attachment; filename=" + fileName);
         #fileName = new String(as.getBytes("GB2312"), "ISO_8859_1"); 
         response['Content-Disposition'] = 'attachment;filename= %s' %filename
         print('attachment;filename='+filename)
         print(1)
         return response
     return big_file_download(request)
