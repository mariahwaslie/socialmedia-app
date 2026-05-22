from django.conf import settings
from django.conf.urls.static import static
from django.urls import path, re_path,include
from . import views

app_name = 'blog'
urlpatterns = [
    path('', views.post_list, name='post_list'),
    path('post/new/', views.PostCreateView.as_view(), name='post_create'),
    path('post/<int:pk>/', views.post_detail, name='post_detail'),
    path('post/<int:pk>/update/', views.EditBlog.as_view(), name='post_update'),
    path('post/<int:pk>/delete/', views.DeleteBlog.as_view(), name='post_delete'),


              ]