from django.conf.urls import url
from django.conf.urls import url
from .import views
from django.conf import settings
from django.views.static import serve
from django.conf.urls.static import static
from . import views as uv

app_name = 'Communication'

urlpatterns = [
    url(r'^search_message/', uv.search_message, name='search_message'),
    url(r'^message_read/', uv.message_read, name='message_read'),
    url(r'^message_by_me/', uv.message_by_me, name='message_by_me'),
    url(r'^marked_message/', uv.marked_message, name='marked_message'),
    url(r'^chat/', uv.chat, name='chat'),
    url(r'^contact_us/', uv.contact_us, name='contact_us'),
    url(r'^write_message/', uv.write_message, name='write_message'),
    url(r'^person_message/', uv.person_message, name='person_message'),
    url(r'^system_message/',uv.system_message,name='system_message'),
    url(r'^(?P<message_id>[0-9]+)/notice_details/$', uv.notice_details, name='notice_details'),
    url(r'^(?P<message_id>[0-9]+)/message_details/$', uv.message_details, name='message_details'),
    url(r'^(?P<message_id>[0-9]+)/mark_by_receiver/$', uv.mark_by_receiver, name='mark_by_receiver'),

]