# chat/routing.py
from . import consumers

from django.urls import re_path

websocket_urlpatterns = [
    re_path(r'ws/single_chat/(?P<pk>\w+)/$', consumers.SingleChatConsumer.as_asgi()),
    re_path(r'ws/chat_room/(?P<pk>\w+)/$', consumers.ChatRoomConsumer.as_asgi()),
]