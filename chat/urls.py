from django.conf import settings
from django.conf.urls.static import static
from django.urls import path, re_path, include
from chat import views
from . import routing
from chat import consumers  # Import the consumers for WebSocket routing

app_name = 'chat'
urlpatterns = [
    # view messages between users
    path('messages/<str:reciver>', views.inbox, name='inbox'),
    path('inbox/', views.inboxlist, name='inboxlist'),
    #create a group
    path('newgroup/',views.CreateGroup.as_view(), name = 'creategroup'),
    # view messages from chat rooms
    path('chatroom/<int:pk>',views.chatroom_messages, name='chatroom'),
    path('update/chatroom/<int:pk>',views.EditChatRoom.as_view(), name='updatechatroom'),
    path('delete/chatroom/<int:pk>', views.DeleteChatroom.as_view(), name='deletechatroom'),
    path('notifications/', views.notifications_view, name='notifications'),
    path('notifications/mark-as-read/<int:notification_id>/', views.mark_notification_as_read,
         name='mark_notification_as_read'),

]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
