from django.urls import path
from search import views
from django.views.generic import TemplateView
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth.views import LoginView, LogoutView
app_name = 'search'
urlpatterns = [
    path('search/', views.search, name='search'),

]