from django.db import models
from django.contrib.contenttypes.models import ContentType
from django.contrib.flatpages.models import FlatPage
from tinymce.models import HTMLField
# Create your models here.


class BibleVersion(models.Model):
    name = models.CharField(max_length=100)
    versionid = models.CharField(max_length=100, blank=True, null=True)
    def __str__(self):
        return self.name
class Book(models.Model):
    name = models.CharField(max_length=100)
    bibleversion = models.ForeignKey(BibleVersion,on_delete=models.CASCADE,default=None,null=True, blank=True,related_name='books')
    # chapter = models.ForeignKey(Chapter, on_delete=models.CASCADE,default=None, related_name='books',blank=True, null=True)
    def __str__(self):
        return self.name
    def get_next_book(self):
        return Book.objects.filter(bibleversion=self.bibleversion, id__gt=self.id).order_by('id').first()

    def get_previous_book(self):
        """Return the previous book in the same BibleVersion."""
        previous_book = Book.objects.filter(
            bibleversion=self.bibleversion,
            id__lt=self.id
        ).order_by('-id').first()
        return previous_book
    def get_chapter_num(self):
        return Chapter.objects.filter(bibleversion=self.bibleversion, book__name=self.name).count()-1


class Chapter(models.Model):
    name = models.CharField(max_length=100)
    number = models.CharField(max_length=100)
    content = HTMLField(default='')
    book= models.ForeignKey(Book, on_delete=models.CASCADE, default=None, related_name='chapter_book',blank=True, null=True)
    bibleversion = models.ForeignKey(BibleVersion,on_delete=models.CASCADE,default=None,null=True, blank=True,related_name='chapter_version')

    def count_chapters(self):
        return (Chapter.objects.filter(bibleversion=self.bibleversion,book=self.book).count())-1
    def next_chapter(self):
            return (int(self.number) + 1)
    def get_number(self):
        if self.number== 'intro':
            return '0'
        return int(self.number)
    def next_chapter_str(self):
        if self.number == 'intro':
            return '1'
        return str(self.number)
    def previous_chapter(self):
        return (int(self.number) - 1)




    def __str__(self):
        return f'{self.name} {self.bibleversion}'

class Verse(models.Model):
    verse_number = HTMLField()
    verse_text = HTMLField(default='')
    Chapter = models.ForeignKey(Chapter, on_delete=models.CASCADE,default=None,null=True, blank=True,related_name='chapter_verses')
    bibleversion = models.ForeignKey(BibleVersion,on_delete=models.CASCADE,default=None,null=True, blank=True,related_name='verse_version')
    book= models.ForeignKey(Book, on_delete=models.CASCADE, default=None, related_name='verse_book',blank=True, null=True)



    def __str__(self):
        return self.verse_text

