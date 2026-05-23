"""
URL configuration for VideoWebsite project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
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
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings
from person.views import *
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
from chat.views import mark_notification_as_read
from user import views as user_views
from person import views as person_views
from chat import consumers
# from playlistapp import urls
# from zmq.backend.cython import message

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('person.urls')),
    path('chat/', include('chat.urls')),
    # path('logout/', CustomLogoutView.as_view(), name='logout'),
    path('blog/', include('blog.urls')),
    path('bible/',include('connect.urls')),
    path('notifications/mark-as-read/<int:notification_id>/', mark_notification_as_read,
         name='mark_notification_as_read'),
    path('submit_comment/<int:id>/', submit_comment, name='submit_comment'),
    path('submit_blog_comment/<int:id>/', submit_blog_comment, name='submit_blog_comment'),
    path('submit_image_comment/<int:id>/', submit_image_comment, name='submit_image_comment'),
    path('submit_video_comment/<int:id>/', submit_video_comment, name='submit_video_comment'),
    path('search',include('search.urls')),
    path('', include('user.urls')),
    path('board/<int:board_id>/reorder/', person_views.reorder_items, name='reorder_items'),
    path('playlist/',include('playlistapp.urls')),
    path('groups/',include('groups.urls'))

    # path('accounts/', include('allauth.urls')),

    # path('', include('socialShare.urls'))  # this is my app urls

]



if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
