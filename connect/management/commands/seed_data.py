from django.core.management.base import BaseCommand
from connect.models import BibleVersion, Book, Chapter
from connect.services import BibleService  # Assuming you have a service to fetch API data
from django.db.models import Q
class Command(BaseCommand):
    help = 'Seed the database with initial data from the API'
    def handle(self, *args, **kwargs):
        bible_versions = BibleVersion.objects.filter(versionid='f72b840c855f362c-04')
        for version in bible_versions:
            books = BibleService.list_books(version.versionid)
            for i,book_data in enumerate(books):
                book = Book.objects.create(
                    name=book_data['name'],
                    bibleversion=version
                    )
                bookid =book_data['id']
                chapters = BibleService.list_chapters(version.versionid, bookid)

                for chapter_data in chapters:
                    chapter = Chapter.objects.create(
                        name=chapter_data['reference'],
                        number=chapter_data['number'],
                        book=book,
                        bibleversion=version
                    )
                    chapter_id=chapter_data['id']
                    chapter_content = BibleService.chapter_contents(version.versionid, chapter_id)
                    if chapter_content['content']:
                        chapter.content = chapter_content['content']
                        chapter.save()

        self.stdout.write(self.style.SUCCESS('Successfully seeded the database'))
