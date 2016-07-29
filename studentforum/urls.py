"""forum URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^home$', views.test, name='test'),
	url(r'^accounts/login/$', views.login, name='forlogin'),
	url(r'^tempt/', views.logout, name='forlogout'),
	url(r'^register/', views.register, name='forregister'),
	url(r'^modify/', views.modifyPassword, name='formodify'),
    url(r'^infoChange/([0-9]+)$', views.changeInfo, name='forchange'),
    url(r'^infoChange/followList/([0-9]+)$', views.showFollow, name='forfollowlist'),
    url(r'^infoChange/fansList/([0-9]+)$', views.showFans, name='forfanslist'),
    url(r'^postDetail/([0-9]+)$', views.showDetail, name='forpostdetail'),
    url(r'^column/([0-9]+)$', views.showColumn, name='forcolumn'),
    url(r'^topic/([0-9]+)$', views.showTopic, name='fortopic'),
    url(r'^follow/([0-9]+)$', views.follow, name='forfollow'),
    url(r'^columnindex/', views.showColumnIndex, name='forcolumnindex'),
    url(r'^topicindex/', views.showTopicIndex, name='fortopicindex'),
    url(r'^$', views.directToHome, name='toHome'),
    url(r'^search/', views.search,name='result'),
    url(r'^download/postattachment/([0-9]+)$',views.downloadpost,name="downloadpost"),
    url(r'^download/replyattachment/([0-9]+)$',views.downloadreply,name="downloadreply"),
    url(r'^postDetail/$',views.countgood,name="countgood"),
    url(r'^postDetail/([0-9]+)/([0-9]+)/([0-9]+)/$',views.postcountgood,name="postcountgood"),
    url(r'^postDetail/([0-9]+)/([0-9]+)/([0-9]+)/([0-9]+)/$',views.postfavor,name="postfavor"),
    url(r'^showReportList$',views.showreportlist,name="showreportlist"),
    url(r'^showtocheckList$',views.showtochecklist,name="showtochecklist"),
    url(r'^showcolumns/', views.showcolumn, name='forshowcolumns'),
    url(r'^letter/([0-9]+)$', views.showLetter, name='forletter'),
    url(r'^letterList/', views.showLetterList, name='forletterlist'),
    
    
    
    
    
    url(r'^userinfo/$',views.delete_account,name='delete_account'),
    url(r'^userinfo/([0-9]+)/$',views.deluser,name='deluser'),
    url(r'^userinfo/([0-9]+)/([0-9]+)/$',views.tocolumnadmin,name='tocolumnadmin'),
    url(r'^userinfo/([0-9]+)/([0-9]+)/([0-9]+)/$',views.setcoladmin,name='setcoladmin'),
    url(r'^userinfo/([0-9]+)/([0-9]+)/([0-9]+)/([0-9]+)/$',views.unsetcoladmin,name='unsetcoladmin'),
    url(r'^userinfo/([0-9]+)/([0-9]+)/([0-9]+)/([0-9]+)/([0-9]+)/$',views.forbiduser,name='forbiduser'),
     
]
