# bible/services.py
import requests
from django.conf import settings
from .models import *
class BibleService:
    @staticmethod
    def get_verse(bible_id, book_id, chapter_id, verse_id):
        url = f"{settings.SCRIPTURE_API_URL}/bibles/{bible_id}/verses/{book_id}.{chapter_id}.{verse_id}"
        headers = {
            'api-key': 'c02d2980c806d125ed22a2009edd21f5'
        }
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            return response.json()
        return None

    @staticmethod
    def list_bibles(id):
        url = f"{settings.SCRIPTURE_API_URL}bibles/{id}"
        headers = {
            'api-key': "c02d2980c806d125ed22a2009edd21f5",
        }
        response = requests.get(url, headers=headers)
        # print(response)
        if response.status_code == 200:
            # print(response.json().get('data', []))  # Debugging: print the response data
            return response.json().get('data')




        print(response.status_code, response.text)  # Debugging: print the error
        return None

    @staticmethod
    def list_books(bibleid):
        url = f"{settings.SCRIPTURE_API_URL}bibles/{bibleid}/books"
        headers = {
            'api-key': "c02d2980c806d125ed22a2009edd21f5",
            'include-chapters-and-sections': 'True',
            'include-chapters':'True'
        }
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            # print(response.json())
            return response.json().get('data')

        print(response.status_code, response.text)  # Debugging: print the error
        return None

    @staticmethod
    def list_chapters(bibleid,bookid):
        url = f"{settings.SCRIPTURE_API_URL}bibles/{bibleid}/books/{bookid}/chapters"
        headers = {
            'api-key': "c02d2980c806d125ed22a2009edd21f5",
            'include-chapters-and-sections': 'True',

        }
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            return response.json().get('data')
        print(response.status_code, response.text)  # Debugging: print the error
        return None
    @staticmethod
    def chapter_contents(bibleid, chapterid):
        url=f"{settings.SCRIPTURE_API_URL}bibles/{bibleid}/chapters/{chapterid}"
        headers = {
            'api-key': "c02d2980c806d125ed22a2009edd21f5",

        }
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            return response.json().get('data')
        print(response.status_code, response.text)
        return None

    @staticmethod
    def get_verses(bibleid,chapterid):
        url = f"{settings.SCRIPTURE_API_URL}bibles/{bibleid}/chapters/{chapterid}/verses"
        headers = {
            'api-key': "c02d2980c806d125ed22a2009edd21f5",

        }
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            return response.json().get('data')
        print(response.status_code, response.text)
        return None

    @staticmethod
    def get_verse(bibleid, verseid):
        url = f"{settings.SCRIPTURE_API_URL}bibles/{bibleid}/verses/{verseid}"
        headers = {
            'api-key': "c02d2980c806d125ed22a2009edd21f5",

        }
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            return response.json().get('data')
        print(response.status_code, response.text)
        return None





