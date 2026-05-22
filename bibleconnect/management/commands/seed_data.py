from django.core.management.base import BaseCommand
from bibleconnect.models import BibleVersion, Book, Chapter
from bibleconnect.services import BibleService  # Assuming you have a service to fetch API data

class Command(BaseCommand):
    help = 'Seed the database with initial data from the API'

    def handle(self, *args, **kwargs):
        bible_versions = BibleService.get_bible_versions()

        for version in bible_versions:
            bible_version, created = BibleVersion.objects.get_or_create(
                versionid=version['id'],
                name=version['name']
            )

            books = BibleService.list_books(version['id'])
            for book_data in books:
                book, created = Book.objects.get_or_create(
                    name=book_data['name'],
                    bibleversion=bible_version
                )

                chapters = BibleService.list_chapters(version['id'], book_data['id'])
                for chapter_data in chapters:
                    chapter, created = Chapter.objects.get_or_create(
                        name=chapter_data['reference'],
                        number=chapter_data['number'],
                        book=book
                    )

                    chapter_content = BibleService.chapter_contents(version['id'], chapter_data['id'])
                    chapter.content = chapter_content['content']
                    chapter.save()

        self.stdout.write(self.style.SUCCESS('Successfully seeded the database'))
