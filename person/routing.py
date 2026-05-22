
from django.urls import re_path,path
from .consumers import NotificationConsumer,CommentConsumer,VideoUploadConsumer

websocket_urlpatterns = [
    re_path(r'ws/notifications/$', NotificationConsumer.as_asgi()),
    re_path(r'ws/comments/(?P<id>\d+)/$', CommentConsumer.as_asgi()),
    path('ws/upload/<str:room_name>/', VideoUploadConsumer.as_asgi()),

]
