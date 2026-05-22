from django.core.management.base import BaseCommand
from bibleconnect.models import BibleVersion, Book, Chapter, Verse
from bibleconnect.services import BibleService  # Assuming you have a service to fetch API data
from django.db.models import Q


bible_versions=[]
class Command(BaseCommand):
    def handle(self, *args, **options):
            bible_versions = BibleVersion.objects.filter(versionid='179568874c45066f-01')
            for version in bible_versions:
                books = BibleService.list_books(version.versionid)
                for i, book_data in enumerate(books):
                    bookid = book_data['id']
                    chapters = BibleService.list_chapters(version.versionid, bookid)
                    for chapter in chapters:
                        chapter_id = chapter['id']
                        verses = BibleService.get_verse(bookid, chapter_id)
                        verse_id = verse_data['id']

                        for verse_data in verses:
                            verse = BibleService.get_verse(bookid, verse_id)
                            if verse['content']:
                                verse_obj = Verse.objects.create(
                                    verse_text=verse['content'],
                                    chapter= chapter,
                                    bibleversion=version,
                                    book= book_data
                                )
                                verse_obj.save()
            self.stdout.write(self.style.SUCCESS('Successfully seeded the database'))









    #
    #
    #
    # for chapter in Chapter.objects.all():
    #         bibleid= chapter.bibleversion.verse.bibleid
    #         chapterid =