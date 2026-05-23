from django.contrib import admin

from bibleconnect.models import *

admin.site.register(Book)
admin.site.register(Chapter)
admin.site.register(BibleVersion)
admin.site.register(Verse)