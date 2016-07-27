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
	url(r'^infoChange/', views.changeInfo, name='forchange'),
    url(r'^postDetail/([0-9]+)$', views.showDetail, name='forpostdetail'),
    url(r'^$', views.directToHome, name='toHome'),
    url(r'^testfile$', views.testfile,name='test1'),
    url(r'^showphoto$', views.showphoto,name='test2'),
    url(r'^showfile$', views.showfile,name='test6'),
    url(r'^testWidget$', views.showWidget,name='test3'),
    url(r'^search/', views.search,name='result'),
    url(r'^testajax/', views.testajax,name='test4'),
    url(r'^testajax2/',views.testajax2,name="test5"),
    url(r'^download/postattachment/([0-9]+)$',views.downloadpost,name="downloadpost"),
    url(r'^download/replyattachment/([0-9]+)$',views.downloadreply,name="downloadreply"),
    url(r'^postDetail/$',views.countgood,name="countgood"),
    url(r'^postDetail/([0-9]+)/([0-9]+)/([0-9]+)/$',views.postcountgood,name="postcountgood"),
    url(r'^showReportList$',views.showreportlist,name="showreportlist"),
    url(r'^showtocheckList$',views.showtochecklist,name="showtochecklist"),
    #url(r'^download/replyattachment/([0-9]+)$',views.testdownload,name="downloadtest")
]
