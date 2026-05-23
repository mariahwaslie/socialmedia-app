# bible/urls.py
from django.urls import path
from . import views
app_name = 'bibleconnect'
urlpatterns = [
    path('verse/', views.get_bible_verse, name='get_bible_verse'),
    path('bibles/', views.list_bibles, name='list_bibles'),
    path('books/<str:bible_id>', views.list_books, name='list_books'),
    path('<str:bible_id>/<str:book>/chapter/<str:chapter_id>', views.read_chapters, name='read_chapter'),
]
