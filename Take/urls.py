from django.contrib import admin
from django.conf.urls import url,include
from django.contrib import admin
from Take import views
from django.conf.urls.static import static
from django.conf import settings
from django.urls import re_path

app_name = 'Take'
urlpatterns = [
    url(r'^task_take/$', views.task_take, name='task_take'),#接单首页的细分类
    url(r'^task_take_division/(?P<task_category>\w+)/$', views.task_take_division, name='task_take_division'),#接单首页的细分类
    url(r'^task_take_division_hot/$', views.task_take_division_hot, name='task_take_division_hot'),#接单首页的热门任务
    url(r'^task_take_division_all/$', views.task_take_division_all, name='task_take_division_all'),#接单首页的所有任务
    url(r'^task_sender_details/(?P<sender_id>\d+)/sender/(?P<task_id>\d+)/$', views.task_sender_details, name='task_sender_details'),#接单首页的所有任务
    url(r'^task_take_division/(?P<task_id>\d+)/fresh/$', views.task_take_division_details, name='task_take_division_details'),#实时更新任务的详情url
    url(r'^task_take_success/(?P<task_id>\d+)/$', views.task_take_success, name='task_take_success'),
    url(r'^task_take_division/Take/task_take_goods/', views.task_take_goods, name='task_take_goods'),
    url(r'^task_take_delete/(?P<good_id>\d+)/$', views.task_take_delete, name='task_take_delete'),

    url(r'^task_take_recommend/', views.task_take_recommend, name='task_take_recommend'),

    url(r'^task_take_tips/', views.task_take_tips, name='task_take_tips'),

    url(r'^task_take_goods/', views.task_take_goods, name='task_take_goods'),
    url(r'^task_take_goods_success/', views.task_take_goods_success, name='task_take_goods_success'),


    url(r'^task_take_competition/$', views.task_take_competition, name='task_take_competition'),
    url(r'^task_take_competition_hot/$', views.task_take_competition_hot, name='task_take_competition_hot'),
    url(r'^task_take_competition/(?P<competition_id>\d+)/$', views.task_take_competition_details, name='task_take_competition_details'),
    url(r'^task_take_competition_collection/$', views.task_take_competition_collection, name='task_take_competition_collection'),

    url(r'^task_take_collection/$', views.task_take_collection, name='task_take_collection'),

    url(r'^task_take_example/$', views.task_take_example, name='task_take_example'),
    url(r'^about_us/$', views.about_us, name='about_us'),
]+static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)