from django.urls import path
from .views import  *
app_name = 'user'
urlpatterns = [

    path('login/', user_login, name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('signup/', SignUpView.as_view(), name='signup'),
    path('profile/update/', UpdateProfile.as_view(), name='updateprofile'),
    path('profile/user/update/<str:pk>', updateUser.as_view(), name='updateuser'),
    path('', indexView.as_view(), name='index'),
    path('profile/', ProfileView.as_view(), name='profile'),
    path('profile/blogs/', ViewBlogs.as_view(), name='profile_blogs'),
    path('profile/prayers/', ViewPosts.as_view(), name='postsview'),
    path('profile/images/', ViewImages.as_view(), name='imagesview'),
    path('profile/videos/', ViewVideos.as_view(), name='myvids'),
    path('profile/history/', ViewHistory.as_view(), name='history'),

]