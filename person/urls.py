from django.urls import path
from person import views
from django.views.generic import TemplateView
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth.views import LoginView, LogoutView
from person.views import *

# Create your views here.
app_name = 'person'

urlpatterns = [

                  path('create/prayer/', views.CreatePost.as_view(), name='post'),
                  path('post/<int:pk>/<int:post_id>/<str:action_type>/', views.viewitem, name='viewpost'),
                  path('edit/prayer/<int:pk>', views.EditPost.as_view(), name='editpost'),

                  path('uploadvideo/', views.UploadVideo.as_view(), name='uploadvideo'),
                  path('video/<int:pk>/<int:video_id>/<str:action_type>/', views.viewvideo, name='viewvideo'),
                  path('edit/video/<int:pk>', views.EditVideo.as_view(), name='editvideo'),

                  # not yet tested
                  path('createpodcast/', views.CreatePodcast.as_view(), name='createpodcast'),
                  path('profile/podcast/', views.ViewPodcats.as_view(), name='podcast'),

                  path('profile/createimage/', views.CreateImage.as_view(), name='createimage'),
                  path('image/<int:pk>/<int:image_id>/<str:action_type>/', views.viewimage, name='viewimage'),
                  path('edit/image/<int:pk>', views.EditImages.as_view(), name='editimage'),

                  path('createboard/', views.CreateBoard.as_view(), name='createboard'),
                  path('viewboard/<str:username>/<int:board_id>', views.boardview, name='viewboard'),
                  path('deleteboard/<int:pk>', views.DeleteBoard.as_view(), name='deleteboard'),

                  # user main page
                  path('<str:username>/<str:action_type>', views.follow_unfollow, name='follow_unfollow_user'),
                  path('profile/following/', views.following_page, name='following'),

                  path('edit/blog/<int:pk>', views.EditBlogPost.as_view(), name='editblogpost'),
                  path('delete/blog/<int:pk>', views.DeleteBlogPosts.as_view(), name='deleteblogpost'),
                  path('prayer/delete/<int:pk>/', views.DeletePosts.as_view(), name='postdelete'),
                  path('video/<int:pk>/delete/', views.DeleteVideo.as_view(), name='videodelete'),
                  path('image/<int:pk>/delete/', views.DeleteImage.as_view(), name='imagedelete'),

                  # work on for user reccomendations system
                  path('profile/explore/', views.explore, name='explore'),

                  path('post/blogview/', views.BlogPostCreate.as_view(), name='createblog'),
                  path('blogpost/<int:pk>/<str:action_type>', views.viewblogpost, name='viewblogpost'),

                  path('prayercomment/<int:pk>/delete', views.CommentDeleteView.as_view(), name='comment-delete'),
                  path('blogcomment/<int:pk>/delete', views.CommentDeleteViewBlog.as_view(), name='delete_blog_comment'),
                  path('videocomment/<int:pk>/delete', views.CommentDeleteViewVideo.as_view(),
                       name='delete_video_comment'),
                  path('imagecomment/<int:pk>/delete', views.CommentDeleteImage.as_view(),
                       name='delete_image_comment'),
                  path('board/<int:board_id>/edit/', views.view_board, name='edit_board'),

                  # path('notifications/', views.notifications_list, name='notifications_list'),
                  # path('submit_comment/<int:id>/', views.submit_comment, name='submit_comment'),


              ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
