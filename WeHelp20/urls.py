"""WeHelp20 URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.conf.urls import include, url
from django.conf import settings
from django.urls import path
from Login import views
from django.views.static import serve
from django.conf.urls.static import static
from Communication import views as uv
from Boards import views as boards_views
from django.contrib.auth import views as auth_views
from Login.views import ForgetPwdView, ResetView,  ModifyPwdView
from django.urls import re_path
from django.views.generic.base import RedirectView
from Send import views as sd
from Take import views as tk

urlpatterns = [
    url(r'^$', views.wehelp, name='wehelp'),
    url(r'^wehelp', views.wehelp, name='wehelp'),
    url('about_platform/', views.about_platform, name='about_platform'),
    url(r'^Send/', include('Send.urls')),
    url(r'^is_login', sd.is_login, name='is_login'),
    url(r'^Take/', include('Take.urls')),
    url(r'^admin/', admin.site.urls),
    url('register/', views.RegisterView.as_view()),
    path('login/', views.LoginView.as_view(),name='login'),
    path('logout/', views.logout_view),
    path('reset_pw/', views.reset_pw),
    path('tags/', views.tags),
    path('tags/new/', views.new_tags),
    path('send/', views.get_orders),
    path('task/', views.get_tasks),
    path('new_avatar/', views.new_avatar, name='new_avatar'),
    path('index/', views.index),
    path('collection/', views.get_collection),
    path('goodfavorite/', views.good_favorite),
    path('collection_c/', views.collection_c),
    path('disclamier/', views.disclaimer),
    path('map/', views.map),
    path('bar/', views.bar),
    path('doughnut/', views.doughnut),
    path('line/', views.line),
    path('linecus/', views.linecus),
    path('pie/', views.pie),
    path('piecus/', views.piecus),
    path('polar/', views.polar),
    path('radar/', views.radar),

    # 验证码以邮箱找回密码
    path("forget/", ForgetPwdView.as_view(), name="forget_pwd"),
    path("captcha/", include('captcha.urls')),
    re_path('reset/(?P<active_code>.*)/', ResetView.as_view(), name="reset_pwd"),
    path("modify/", ModifyPwdView.as_view(), name="modify_pwd"),

    url(r'^Communication/', include('Communication.urls')),

    url(r'^chat/', include('chat.urls')),

    url(r'^about_platform',uv.about_platform, name='about_platform'),
    url(r'^about_us/$', tk.about_us, name='about_us'),

    #url(r'^search',uv.search,name='search'),

    url(r'^media/(?P<path>.*)$', serve, {'document_root': settings.MEDIA_ROOT}),

    url(r'^luntan/$', boards_views.BoardListView.as_view(), name='luntan'),
    url(r'^search_subject/$', boards_views.search_subject, name='search_subject'),
    url(r'^boards/(?P<pk>\d+)/$', boards_views.TopicListView.as_view(), name='board_topics'),
    url(r'^boards/(?P<pk>\d+)/new/$', boards_views.new_topic, name='new_topic'),
    url(r'^boards/(?P<pk>\d+)/topics/(?P<topic_pk>\d+)/$', boards_views.PostListView.as_view(),
                      name='topic_posts'),
    url(r'^boards/(?P<pk>\d+)/topics/(?P<topic_pk>\d+)/reply/$', boards_views.reply_topic, name='reply_topic'),
    url(r'^boards/(?P<pk>\d+)/topics/(?P<topic_pk>\d+)/complain/$', boards_views.complain, name='complain'),
    url(r'^boards/(?P<pk>\d+)/topics/(?P<topic_pk>\d+)/luntanuser/$', boards_views.luntanuser,name='luntanuser'),
    url(r'^boards/(?P<pk>\d+)/topics/(?P<topic_pk>\d+)/posts/(?P<post_pk>\d+)/edit/$',
                      boards_views.PostUpdateView.as_view(), name='edit_post'),
    url(r'^edit_post2/$', boards_views.edit_post2, name="edit_post2"),
    url(r'^new_topic2/$', boards_views.new_topic2, name='new_topic2'),
    url(r'^complain2/$', boards_views.complain2, name="complain2"),
    url(r'^delete/$', boards_views.delete2, name='delete2'),
    url(r'^contact_us/$', boards_views.contact_us, name='contact_us'),
    url(r'^contact_way/$', boards_views.contact_way, name="contact_way"),
    url(r'^cooperation/$', boards_views.cooperation, name="cooperation"),
    url(r'^joinus/$', boards_views.joinus, name="joinus"),
    url(r'^boards/(?P<pk>\d+)/top/$', boards_views.top, name='top'),

    # 添加网站小图标
     url(r'^favicon.ico$', RedirectView.as_view(url=r'static/favicon.ico')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
