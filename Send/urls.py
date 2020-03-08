from django.conf.urls import url
from .import views
from django.conf import settings
from django.views.static import serve
from django.conf.urls.static import static

app_name = 'Send'
urlpatterns = [


    url(r'^send_category', views.send_category, name='send_category'),
    url(r'^add_order', views.add_order, name='add_order'),
    url(r'^filling_suc', views.filling_suc, name='filling_suc'),
    url(r'^(?P<task_id>[0-9]+)/send_details/$', views.send_details, name='send_details'),
    url(r'^(?P<task_id>[0-9]+)/reset/', views.reset, name='reset'),

    url(r'^recommend_master', views.recommend_master, name='recommend_master'),
    url(r'^popular_master', views.popular_master, name='popular_master'),
    url(r'^(?P<master_type_id>[0-9]+)/masters_category/$', views.master_category, name='master_category'),
    url(r'^masters', views.masters, name='masters'),
    url(r'^(?P<master_id>[0-9]+)/master_details/$', views.master_details, name='master_details'),
    url(r'^(?P<master_id>[0-9]+)/add_order_of_master/$', views.add_order_of_master, name='add_order_of_master'),
    url(r'^master_like', views.master_like, name='master_like'),
    url(r'^master_favorite$', views.master_favorite, name='master_favorite'),
    url(r'^(?P<task_id>[0-9]+)/del_send_suc$', views.del_send_suc, name='del_send_suc'),

    url(r'^recommend_good', views.recommend_good, name='recommend_good'),
    url(r'^popular_good', views.popular_good, name='popular_good'),
    url(r'^(?P<good_type_id>[0-9]+)/good_category/$', views.good_category, name='good_category'),
    url(r'^goods', views.goods, name='goods'),
    url(r'^(?P<good_id>[0-9]+)/good_details/$', views.good_details, name='good_details'),
    url(r'^good_favorite/$', views.good_favorite, name='good_favorite'),
    url(r'^add_car', views.add_car, name='add_car'),

    url(r'^add_competition', views.add_competition, name='add_competition'),
    url(r'^suc', views.suc, name='suc'),
    url(r'^reset', views.reset, name='reset'),

    url(r'^media/(?P<path>.*)$', serve, {'document_root': settings.MEDIA_ROOT}),



] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
