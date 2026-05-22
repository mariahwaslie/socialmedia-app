from .views import *
from django.urls import path

app_name = 'faith'
urlpatterns = [

    path('request/group/', create_group_request, name='create_group_request'),
    path('review/requests/', review_group_requests, name='review_group_requests'),
    path('approve/group/request/<int:request_id>/', approve_group_request, name='approve_group_request'),
    path('deny/group/request/<int:request_id>/', deny_group_request, name='deny_group_request'),
    path('group/<int:group_id>', group_details, name='group_details'),
    path('groups/', group_list, name='group_list'),
    path('join_group/<int:group_id>/<int:user_id>', join_group, name='join_group'),
    path('group/join/request/<int:group_id>/', request_to_join, name='request_to_join'),
    path('group/join/denied/<int:group_id>', deny_group_join, name='deny_group_join'),

    path('group/create/post/<int:group_id>/', create_post, name='create_group_post'),
    path('group/create/prayer/<int:group_id>/', create_prayer, name='create_prayer'),
    path('group/create/image/<int:group_id>/', create_image, name='create_image'),
    path('group/create/video/<int:group_id>/', create_video, name='create_video'),

    path('event/create/<int:group_id>', create_event, name='create_event'),
    path('event/<int:pk>/edit/', update_event, name='update_event'),
    # path('location/<int:id>', LocationView.as_view(), name='location' )
    path('request/church/', create_church_request, name='create_church_request'),

]
