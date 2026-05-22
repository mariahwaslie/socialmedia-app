# bible/views.py
import json
from .models import *

from django.shortcuts import render
from .services import BibleService
from user.models import Profile
from django.contrib.auth.models import User


def get_bible_verse(request):
    bible_id = request.GET.get('bible_id', 'de4e12af7f28f599-02')  # ESV Bible as default
    book_id = request.GET.get('book_id', 'JHN')  # John as default
    chapter_id = request.GET.get('chapter_id', '3')
    verse_id = request.GET.get('verse_id', '16')
    verse_data = BibleService.get_verse(bible_id, book_id, chapter_id, verse_id)
    return render(request, 'verse.html', {'verse_data': verse_data})


def list_bibles(request):
    if request.user.is_authenticated:
        user = request.user
        profile = Profile.objects.get(user=user)
    else:
        profile = None
        user = None
    list_bibles = BibleVersion.objects.all()

    context = {

        'list_bibles': list_bibles,
        'user': user,
        'profile': profile
    }
    return render(request, 'bibles.html', context)


def list_books(request, bible_id):
    if request.user.is_authenticated:
        user = request.user
        profile = Profile.objects.get(user=user)
    else:
        profile = None
        user = None
    biblever = BibleVersion.objects.get(versionid=bible_id)
    list_books = Book.objects.filter(bibleversion=biblever).prefetch_related('chapter_book').all()

    context = {
        'list_books': list_books,
        'user': user,
        'profile': profile
    }
    return render(request, 'books.html', context)


def read_chapters(request, bible_id, book, chapter_id):
    if request.user.is_authenticated:
        user = request.user
        profile = Profile.objects.get(user=user)
    else:
        profile = None
        user = None



    biblever = BibleVersion.objects.get(versionid=bible_id)
    # book= Book.objects.get(versionid=biblever,name=book)

    chapter = Chapter.objects.get(bibleversion=biblever, book__name=book, number=chapter_id)
    biblever = BibleVersion.objects.get(versionid=bible_id)
    first_book = Book.objects.filter(bibleversion=biblever).first()

    context = {'chapter': chapter, 'fbook': first_book, 'user': user,
               'profile': profile}
    return render(request, 'chapters.html', context)
