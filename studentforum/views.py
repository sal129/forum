
from django import forms
from django.shortcuts import render, render_to_response
from .forms import LoginForm, RegisterForm, changeForm, userForm, PasswordForm, PostForm, ReplyForm,LetterForm,EditColumnForm, AddColumnForm
from django.contrib import auth
from django.http import HttpResponseRedirect, HttpResponse, StreamingHttpResponse
from django.contrib.auth.models import User
from .models import MyUser, Post, Reply, ReplytoReply, PostTotal, Column, Topic, Letter
from django.core.urlresolvers import reverse
from django.views.decorators.csrf import ensure_csrf_cookie
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _
from itertools import chain
import os
import json
import codecs
# Create your views here.
def test(request):
    hotColumns = Column.objects.order_by("-pstNum")
    hotTopics = Topic.objects.order_by("-pstNum")
    posts = Post.objects.order_by('-latestupdate')
    form = PostForm()
    if request.user.is_authenticated():
        if request.method == 'POST':
            params = request.POST
            form = PostForm(request.POST, request.FILES)
            if form.is_valid():
                post = form.save(commit = False)
                post.author = request.user.myuser
                post.save()
                fortotal = PostTotal()
                fortotal.type1 = 0
                fortotal.forpost = post
                fortotal.save()
                form = PostForm()
            posts = Post.objects.order_by('-latestupdate')
            return render(request,'studentforum/afterLogHome.html', {'posts': posts,'form':form, 'hotColumns': hotColumns, 'hotTopics': hotTopics})
        else:
            return render(request,'studentforum/afterLogHome.html', {'posts': posts,'form':form, 'hotColumns': hotColumns, 'hotTopics': hotTopics})
    else:
        return render(request,'studentforum/home.html', {'posts': posts,'form':form, 'hotColumns': hotColumns, 'hotTopics': hotTopics})
	
	
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
    form = PasswordForm()
    if request.user.is_authenticated():
        if request.method == 'POST':
            form = PasswordForm(request.POST)
            if form.is_valid():
                oldpassword = request.POST['oldpassword']
                user = auth.authenticate(username=request.user.username, password=oldpassword)
                if user is not None and user.is_active:
                    request.user.set_password(request.POST['password'])
                    request.user.save()
                    return HttpResponseRedirect("/home")
                else:
                    msg = "输入的原密码错误"
                    form.add_error('oldpassword', msg)
                return render(request, "studentforum/modify.html",{'form': form})
            else:
                return render(request, "studentforum/modify.html",{'form': form})
        else:
            return render(request, "studentforum/modify.html",{'form': form})
    else:
        return HttpResponseRedirect("/home")

def changeInfo(request, infoIDstr):
    infoID = int(infoIDstr)
    ofUser = User.objects.get(id = infoID).myuser
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
               if 'portrait' in request.FILES:
                    request.user.myuser.portrait = form.cleaned_data['portrait']
               request.user.myuser.save()
               request.user.save()
               form = changeForm(instance = request.user.myuser)
               form1 = userForm(instance = request.user)
        form = changeForm(instance = request.user.myuser)
        form1 = userForm(instance = request.user)
        return render(request, "studentforum/infoChange.html", {'form': form, 'form1': form1, 'user': ofUser})
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
    hotColumns = Column.objects.order_by("-pstNum")
    hotTopics = Topic.objects.order_by("-pstNum")
    post = Post.objects.get(id = int(postIDstr))
    if request.is_ajax() and request.user.is_authenticated() and not request.user.myuser.isforbidden:
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
            fortotal.forreplytoreply = reptorep1
            fortotal.save()
            return HttpResponse(json.dumps({"content":reptorep1.content,"author":reptorep1.author.user.username,"reptorep":reptorep1.id}))
        elif req["type"] == "reportpost":
            post = Post.objects.get(id = int(req["postid"]))
            tempt = Post.objects.get(id = int(req["postid"])).posttotal
            tempt.type = 0
            if not request.user.myuser in post.reportposts.all():
                request.user.myuser.reportPst.add(post)
                if tempt.reportNum == 0:
                    #print("1")
                    tempt.firstReportTime = timezone.now()
                    tempt.reportNum = 1
                elif tempt.ischecked==True:
                    tempt.firstReportTime = timezone.now()
                    tempt.reportNum = tempt.reportNum + 1
                    tempt.ischecked = False
                else:
                    #print("2")
                    tempt.reportNum = tempt.reportNum + 1
                print(tempt.reportNum)
                tempt.save()
                print(tempt)
            return HttpResponse(json.dumps({"content":""}))  
        elif req["type"] == "reportreply":
            reply = Reply.objects.get(id = int(req["replyid"]))
            tempt = Reply.objects.get(id = int(req["replyid"])).posttotal
            tempt.type = 1
            if not request.user.myuser in reply.reportreplies.all():
                request.user.myuser.reportRst.add(reply)
                if tempt.reportNum == 0:
                    #print("1")
                    tempt.firstReportTime = timezone.now()
                    tempt.reportNum = 1
                else:
                    #print("2")
                    tempt.reportNum = tempt.reportNum + 1
                print(tempt.reportNum)
                tempt.save()
                print(tempt)
            return HttpResponse(json.dumps({"content":""}))
        elif req["type"] == "reportreplytoreply":
            reptorep = ReplytoReply.objects.get(id = int(req["reptorepid"]))
            tempt = ReplytoReply.objects.get(id = int(req["reptorepid"])).posttotal
            tempt.type = 2
            if not request.user.myuser in reptorep.reportreptorep.all():
                request.user.myuser.reportRpytoRpy.add(reptorep)
                if tempt.reportNum == 0:
                    #print("1")
                    tempt.firstReportTime = timezone.now()
                    tempt.reportNum = 1
                else:
                    #print("2")
                    tempt.reportNum = tempt.reportNum + 1
                print(tempt.reportNum)
                tempt.save()
                print(tempt)
            return HttpResponse(json.dumps({"content":""}))
        elif req["type"] == "deletereply":
            reply = Reply.objects.get(id = int(req["replyid"]))
            print(PostTotal.objects.all())
            print(Reply.objects.all())
            reply.delete()
            print(PostTotal.objects.all())
            print(Reply.objects.all())
            return HttpResponse(json.dumps({"content":""}))  
        elif req["type"] == "deletereptorep":
            print("receive")
            reptorep = ReplytoReply.objects.get(id = int(req["reptorepid"]))
            print(PostTotal.objects.all())
            print(ReplytoReply.objects.all())
            reptorep.delete()
            print(PostTotal.objects.all())
            print(ReplytoReply.objects.all())
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
            if form.is_valid() and request.user.is_authenticated() and not request.user.myuser.isforbidden:
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
                fortotal.forreply = reply
                fortotal.save()
        elif 'delete' in request.POST:
            post = Post.objects.get(id = int(postIDstr))
            column = post.ofColumn
            post.delete()
            print(Column.objects.all())
            return HttpResponseRedirect(reverse("forcolumn",args=[column.id])) 



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

    isfavor=False
    if request.user.is_authenticated():
	    if request.user.myuser.collectPst.filter(id=post.id).exists():
	        isfavor=True
        
    return render(request, 'studentForum/postDetail.html', {'replies': replies, 'post': post, 'postfilename':postfilename,'form': form,'replylist': replylist, 'isfavor':isfavor, 'hotColumns': hotColumns, 'hotTopics': hotTopics})

def directToHome(request):
	return HttpResponseRedirect("/home")

def showLetter(request, toIDstr):
    toID = int(toIDstr)
    toUser = User.objects.get(id = toID).myuser
    larams = request.POST if request.method == 'POST' else None
    form = LetterForm(larams)
    if form.is_valid() and request.user.is_authenticated():
        letter = form.save(commit = False)
        letter.userFrom = request.user.myuser
        letter.userTo = toUser
        letter.save()
        form = LetterForm()
    letters1 = Letter.objects.filter(userFrom = request.user.myuser).filter(userTo = toUser)
    letters2 = Letter.objects.filter(userFrom = toUser).filter(userTo = request.user.myuser)
    letters = letters1 | letters2
    return render(request, 'studentForum/letter.html', {'letters': letters, 'form': form, 'user': toUser})

def showLetterList(request):
    userSet = set()
    for letter in request.user.myuser.reverse_from.all():
        userSet.add(letter.userTo)
    for letter in request.user.myuser.reverse_to.all():
        userSet.add(letter.userFrom)
    return render(request, 'studentForum/letterlist.html', {'users': userSet})

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
    posts = Post.objects.filter(ofColumn = Column.objects.get(id = columnID)).order_by('-latestupdate')
    hotColumns = Column.objects.order_by("-pstNum")
    hotTopics = Topic.objects.order_by("-pstNum")
    form = PostForm()
    if request.user.is_authenticated() and not request.user.myuser.isforbidden:
        params = request.POST if request.method == 'POST' else None
        form = PostForm(request.POST,request.FILES)
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
            fortotal = PostTotal()
            fortotal.type1 = 0
            fortotal.forpost = post
            fortotal.save()
            form = PostForm()
            posts = Post.objects.filter(ofColumn = Column.objects.get(id = columnID)).order_by('-latestupdate')
        temp = Column.objects.get(id = columnID)
        temp.pstNum = posts.count()
        temp.save()
        return render(request, 'studentForum/column.html', {'posts': posts, 'form': form, 'column': temp, 'hotColumns': hotColumns, 'hotTopics': hotTopics})
    else:
        temp = Column.objects.get(id = columnID)
        temp.pstNum = posts.count()
        temp.save()
        return render(request, 'studentForum/column.html', {'posts': posts, 'form': form, 'column': temp, 'hotColumns': hotColumns, 'hotTopics': hotTopics})

def follow(request, followIDstr):
    followID = int(followIDstr)
    ofUser = User.objects.get(id = followID).myuser
    currentUser = request.user.myuser
    if ofUser in currentUser.follow.all():
        currentUser.follow.remove(ofUser)
        currentUser.followNum -= 1
        ofUser.fansNum -= 1
        ofUser.save()
        currentUser.save()
        return HttpResponseRedirect("/infoChange/" + str(followID))
    currentUser.follow.add(ofUser)
    currentUser.followNum += 1
    ofUser.fansNum += 1
    ofUser.save()
    currentUser.save()
    return HttpResponseRedirect("/infoChange/" + str(followID))

def showFollow(request, userIDstr):
    userID = int(userIDstr)
    tempUser = User.objects.get(id = userID)
    follow = tempUser.myuser.follow.all()
    return render(request, 'studentForum/followlist.html', {'follow': follow, 'user': tempUser.myuser})

def showFans(request, userIDstr):
    userID = int(userIDstr)
    tempUser = User.objects.get(id = userID)
    fans = tempUser.myuser.myuser_set.all()
    return render(request, 'studentForum/fanslist.html', {'fans': fans, 'user': tempUser.myuser})

def showActions(request, userIDstr):
    userID = int(userIDstr)
    tempUser = User.objects.get(id = userID)
    actionSet = set()
    for post in Post.objects.filter(author = tempUser.myuser):
        actionSet.add(post.posttotal)
    for reply in Reply.objects.filter(author = tempUser.myuser):
        actionSet.add(reply.posttotal)
    for replytoreply in ReplytoReply.objects.filter(author = tempUser.myuser):
        actionSet.add(replytoreply.posttotal)
    actionList = list(actionSet)
    actionList.reverse()
    print(actionList)
    return render(request, 'studentForum/showactions.html', {'user': tempUser.myuser, 'actions': actionList})

def showCollects(request, userIDstr):
    userID = int(userIDstr)
    tempUser = User.objects.get(id = userID)
    collects = tempUser.myuser.collectPst.all()
    return render(request, 'studentForum/showcollects.html', {'user': tempUser.myuser, 'collects': collects})


def showColumnIndex(request):
    hotColumns = Column.objects.order_by("-pstNum")
    hotTopics = Topic.objects.order_by("-pstNum")
    columns = Column.objects.all()
    return render(request, 'studentForum/columnindex.html', {'columns': columns, 'hotColumns': hotColumns, 'hotTopics': hotTopics})

def showTopic(request, topicIDstr):
    hotColumns = Column.objects.order_by("-pstNum")
    hotTopics = Topic.objects.order_by("-pstNum")
    topicID = int(topicIDstr)
    topic = Topic.objects.get(id = topicID)
    posts = Post.objects.filter(ofTopic = topic).order_by('-latestupdate')
    topic.pstNum = posts.count()
    return render(request, 'studentForum/topic.html', {'posts': posts, 'topic': topic, 'hotColumns': hotColumns, 'hotTopics': hotTopics})

def showTopicIndex(request):
    hotColumns = Column.objects.order_by("-pstNum")
    hotTopics = Topic.objects.order_by("-pstNum")
    topics = Topic.objects.all()
    return render(request, 'studentForum/topicindex.html', {'topics': topics, 'hotColumns': hotColumns, 'hotTopics': hotTopics})

def search(request):
    hotColumns = Column.objects.order_by("-pstNum")
    hotTopics = Topic.objects.order_by("-pstNum")
    key = request.GET['q']
    posts1 = Post.objects.filter(title__icontains=key)
    posts2 = Post.objects.filter(content__icontains=key)
    posts = posts1 | posts2
    return render(request,'studentForum/result.html',{'posts':posts, 'hotColumns': hotColumns, 'hotTopics': hotTopics})




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
            return HttpResponse(json.dumps({"num":user.collectPstNum,"message":"取消收藏"}))
        if str(req["target"]) == "exclude":
            #global req
            req=json.loads(request.POST["data"])
            post=Post.objects.get(id=int(req["postid"]))
            user=request.user.myuser
            user.collectPst.remove(post)
            tmp=user.collectPstNum-1
            user.collectPstNum=tmp
            user.save()
            print(user.collectPstNum)
            print("this is exclude")
            return HttpResponse(json.dumps({"num":user.collectPstNum,"message":"收藏"}))

def showreportlist(request):

    # posts = []
    # for posttempt1 in posttempt:
    #     posts.append({"reportinside":posttempt1.forpost,"posttotal":})
    # print(posts) 
     if request.method == 'POST':
        if "post" in request.POST:
            postid = int(request.POST["id"])
            listtempt = []
            if listtempt:
                print("understanderror")
            if Post.objects.all().filter(id = postid):
                print(Reply.objects.all())
                print(ReplytoReply.objects.all())
                tempt = Post.objects.all().get(id = postid)
                tempt.delete()
                print(Reply.objects.all())
                print(ReplytoReply.objects.all())
        elif "reply" in request.POST:
            replyid = int(request.POST["id"])
            if Reply.objects.all().filter(id = replyid):
                tempt = Reply.objects.all().get(id = replyid)
                tempt.delete()
        elif "replytoreply" in request.POST:
            reptorepid = int(request.POST["id"])
            if ReplytoReply.objects.all().filter(id = reptorepid):
                tempt = ReplytoReply.objects.all().get(id = reptorepid)
                tempt.delete()
        elif "passcheck" in request.POST:
            id1 = int(request.POST["id"])
            if(request.POST["type"] == "post"):
                if Post.objects.all().filter(id = id1):
                    print("postpass")
                    tempt = Post.objects.all().get(id = id1).posttotal
                    tempt.ischecked = True
                    tempt.save()
            elif(request.POST["type"] == "reply"):
                if Reply.objects.all().filter(id = id1):
                    tempt = Reply.objects.all().get(id = id1).posttotal
                    tempt.ischecked = True
                    tempt.save()
            elif(request.POST["type"] == "replytoreply"):
                if ReplytoReply.objects.all().filter(id = id1):
                    tempt = ReplytoReply.objects.all().get(id = id1).posttotal
                    tempt.ischecked = True      
                    tempt.save() 

     posts1 = PostTotal.objects.all().filter(reportNum__gt = 0)
     posts2 = PostTotal.objects.all().filter(ischecked= False)
     posts = (posts1 & posts2).order_by('firstReportTime')

            #return render(request, 'studentForum/showphoto.html',{'photo':photo})
     return render(request, 'studentForum/reportpostlist.html', {'posts': posts})

def showtochecklist(request):

    # posts = []
    # for posttempt1 in posttempt:
    #     posts.append({"reportinside":posttempt1.forpost,"posttotal":})
    # print(posts) 
     if request.method == 'POST':
        if "post" in request.POST:
            postid = int(request.POST["id"])
            listtempt = []
            if listtempt:
                print("understanderror")
            if Post.objects.all().filter(id = postid):
                print(Reply.objects.all())
                print(ReplytoReply.objects.all())
                tempt = Post.objects.all().get(id = postid)
                tempt.delete()
                print(Reply.objects.all())
                print(ReplytoReply.objects.all())
        elif "reply" in request.POST:
            replyid = int(request.POST["id"])
            if Reply.objects.all().filter(id = replyid):
                tempt = Reply.objects.all().get(id = replyid)
                tempt.delete()
        elif "replytoreply" in request.POST:
            reptorepid = int(request.POST["id"])
            if ReplytoReply.objects.all().filter(id = reptorepid):
                tempt = ReplytoReply.objects.all().get(id = reptorepid)
                tempt.delete()
        elif "passcheck" in request.POST:
            id1 = int(request.POST["id"])
            if(request.POST["type"] == "post"):
                if Post.objects.all().filter(id = id1):
                    print("postpass")
                    tempt = Post.objects.all().get(id = id1).posttotal
                    tempt.ischecked = True
                    tempt.save()
            elif(request.POST["type"] == "reply"):
                if Reply.objects.all().filter(id = id1):
                    tempt = Reply.objects.all().get(id = id1).posttotal
                    tempt.ischecked = True
                    tempt.save()
            elif(request.POST["type"] == "replytoreply"):
                if ReplytoReply.objects.all().filter(id = id1):
                    tempt = ReplytoReply.objects.all().get(id = id1).posttotal
                    tempt.ischecked = True      
                    tempt.save() 

     posts = PostTotal.objects.all().filter(ischecked= False).order_by('publishTime')

            #return render(request, 'studentForum/showphoto.html',{'photo':photo})
     return render(request, 'studentForum/tochecklist.html', {'posts': posts})



def showcolumn(request):
    form1= EditColumnForm()
    form2 = AddColumnForm()
    inlineid = -1
    if request.method == 'POST'and request.user.is_authenticated():
        if "change" in request.POST:
            form1 = EditColumnForm(request.POST)
            if form1.is_valid():
                column = Column.objects.all().get(id = int(request.POST["change"]))
                column.name = request.POST["value"]
                column.save()
                form1= EditColumnForm()
            else:
                inlineid = int(request.POST["change"])
                print(inlineid)
        elif "add" in request.POST:
            form2 = AddColumnForm(request.POST)
            if form2.is_valid():
                newone = Column()
                newone.name = request.POST["value"]
                newone.save()
                form2 = AddColumnForm()
        elif "delete" in request.POST:
            print(Post.objects.all())
            column = Column.objects.all().get(id = int(request.POST["delete"]))
            column.delete()
            print(Post.objects.all())
    colunmns = Column.objects.all()    
    return render(request, 'studentForum/showcolumnlist.html', {'columns': colunmns,'form1':form1,'form2':form2,"inlineid":inlineid})


def deluser(request,uid):
    user=MyUser.objects.get(user_id=uid)
    
    user.isdeleted=True
    user.manageType=0
    
    user.save()
    usergroup=MyUser.objects.all()
    print('whatthehell')
    print(user.isdeleted)
    for u in usergroup:
        print(u.user_id)
        print(u.isdeleted)
        
    columngroup=Column.objects.all()
    for col in columngroup:
        
        for adm in col.manager.all():
            if adm.user_id==uid:
                col.manager.remove(adm)
                col.save()
    for col in columngroup:
        print("this is column {0}".format(col.name))
        for adm in col.manager.all():
            print(adm.user.username)
    return render(request,'studentForum/userinfo.html',{'usergroup':usergroup})
def forbiduser(request,uid,w,h,a,t):
    user=MyUser.objects.get(user_id=uid)
    user.isforbidden=True
    user.manageType=0
    user.save()
    usergroup=MyUser.objects.all()
    return render(request,'studentForum/userinfo.html',{'usergroup':usergroup})
def tocolumnadmin(request,uid,whatever):
    user=MyUser.objects.get(user_id=uid)
    if user.manageType==0:
        
        user.manageType=1
    elif user.manageType==1:
        user.manageType=0
    user.save()
    usergroup=MyUser.objects.all()
    columngroup=Column.objects.all()
    return render(request,'studentForum/userinfo.html',{'usergroup':usergroup,'columngroup':columngroup})
def delete_account(request):
    usergroup=MyUser.objects.all()
    #for user in usergroup:
        #print(user.user.id)
    # user=MyUser.objects.get(user_id=1)
    return render(request,'studentForum/userinfo.html',{'usergroup':usergroup})
    #return render(request,'studentForum/usermanage.html',{'user':user})
    #user=MyUser.user.filter(id=userid)
    #print 
def setcoladmin(request,uid,cid,whatever):
    
    #print('wahtaer')
    aduser=MyUser.objects.get(user_id=uid)
    #print(aduser.user.username)
    col=Column.objects.get(id=cid)
    col.manager.add(aduser)
    usergroup=MyUser.objects.all()
    columngroup=Column.objects.all()
    colmanager=col.manager.all()
    
    for col in columngroup:
        print("this is column {0}".format(col.name))
        for adm in col.manager.all():
            print(adm.user.username)
    return render(request,'studentForum/userinfo.html',{'usergroup':usergroup,'columngroup':columngroup,'colmanager':colmanager,'colname':col.name})
def unsetcoladmin(request,uid,cid,w,hatever):
    aduser=MyUser.objects.get(user_id=uid)
    col=Column.objects.get(id=cid)
    col.manager.remove(aduser)
    usergroup=MyUser.objects.all()
    columngroup=Column.objects.all()
    colmanager=col.manager.all()
    
    for col in columngroup:
        print("this is column {0}".format(col.name))
        for adm in col.manager.all():
            print(adm.user.username)
    return render(request,'studentForum/userinfo.html',{'usergroup':usergroup,'columngroup':columngroup,'colmanager':colmanager,'colname':col.name})

def center(request):
    if request.user.myuser.manageType != 2:
        return HttpResponseRedirect("/home")
    else:
        return render(request, 'studentforum/center.html')
 # user = auth.authenticate(username=username, password=oldpassword)
 #            if user is not None and user.is_active:
 #                newpassword = request.POST.get('newpassword1', '')
 #                user.set_password(newpassword)
 #                user.save()
 #                return render_to_response('index.html', RequestContext(request,{'changepwd_success':True}))