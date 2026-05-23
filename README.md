# Social Media App

A Django social media project centered on faith-based sharing, community groups, Bible reading, and real-time messaging. The app lets users create profiles, follow or block other users, publish prayers, images, videos, blogs, podcasts, organize content into boards and playlists, join groups/church groups, search across content, and chat through Django Channels WebSockets.

## Project Status

This repository contains the Django project package, app code, templates, migrations, and a sample fixture (`data.json`). One required runtime file is not currently committed:

- `VideoWebsite/settings.py`

`manage.py`, `VideoWebsite/asgi.py`, and `VideoWebsite/wsgi.py` all expect `DJANGO_SETTINGS_MODULE=VideoWebsite.settings`, so the project cannot run until that settings module is restored or recreated locally.

The package names and Django app labels have been normalized around the repository folders: `connect` for Bible-related data/views and `groups` for group/church-group features.

## Main Features

- User accounts with signup, login, profile editing, profile pictures, follows, blocking, and profile history.
- Social content for prayers, rich text posts, images, videos, blog posts, and podcasts.
- Likes, views, saves, comments, threaded comments for videos/blogs, and notification events through `django-notifications-hq`.
- Boards that collect images, videos, prayers, and blog posts with ordered through models and drag/reorder support.
- Video playlists with ordered playlist items.
- Public/followers-only/private content privacy choices across core content types.
- Search across users, prayers, blog posts, images, videos, and categories/tags.
- Groups and church groups with membership roles, join requests, group creation requests, posting controls, and events.
- Real-time single and group chat using Django Channels consumers.
- Bible version/book/chapter models, API-backed Bible lookup services, and management commands for seeding Bible data.
- Text-similarity recommendations using scikit-learn TF-IDF/cosine similarity for posts, videos, images, and blog posts.

## Tech Stack

- Python and Django 4.2
- Django Channels and Daphne for ASGI/WebSockets
- Redis support through `channels-redis`
- SQLite by default in local Django projects, with `psycopg2-binary` available for PostgreSQL
- TinyMCE/CKEditor packages for rich text editing
- `django-notifications-hq` for in-app notifications
- scikit-learn, TensorFlow/Keras, BeautifulSoup, NumPy, and related libraries for similarity/search helpers
- Bootstrap packages and template-based server-rendered UI

## Repository Layout

```text
VideoWebsite/     Project URL routing plus ASGI/WSGI entry points
user/             Authentication, profiles, follows, blocking, and profile dashboards
person/           Core social content: prayers, posts, images, videos, podcasts, boards, comments, recommendations
chat/             Direct messages, chat rooms, notifications view, and WebSocket consumers
groups/           Groups, church groups, memberships, join requests, group content, and events
connect/          Bible versions, books, chapters, verses, API services, and seed commands
blog/             Separate simple blog app with CRUD views
playlistapp/      Video playlists and ordered playlist items
search/           Cross-content search view and template
templates/        Shared site templates such as base, index, login, signup, logout
data.json         Sample/development fixture data
requirements.txt  Python dependency pins
```

## Important Routes

- `/` - home/profile entry points from `person` and `user`
- `/login/`, `/logout/`, `/signup/` - authentication
- `/profile/` - current user profile dashboard
- `/create/prayer/`, `/uploadvideo/`, `/profile/createimage/`, `/post/blogview/` - content creation
- `/chat/inbox/`, `/chat/messages/<username>`, `/chat/chatroom/<id>` - messaging
- `/groups/groups/`, `/groups/request/group/`, `/groups/request/church/` - groups and church group flows
- `/bible/bibles/`, `/bible/books/<bible_id>`, `/bible/<bible_id>/<book>/chapter/<chapter_id>` - Bible views
- `/playlist/create/`, `/playlist/<id>/`, `/playlist/<id>/add/` - playlists
- `/search/search/?search=<query>` - search

The groups URLs are mounted at `/groups/`, and their Django URL namespace is `groups`.

## Local Setup

1. Create and activate a virtual environment.

   ```bash
   python -m venv .venv
   source .venv/bin/activate
   ```

2. Install dependencies.

   ```bash
   pip install -r requirements.txt
   ```

3. Restore or create `VideoWebsite/settings.py`.

   At minimum, the settings module needs:

   - `SECRET_KEY`, `DEBUG`, `ALLOWED_HOSTS`
   - `INSTALLED_APPS` entries for the Django apps in this repo and third-party apps in `requirements.txt`
   - database configuration
   - `STATIC_URL`, `STATIC_ROOT`, `MEDIA_URL`, `MEDIA_ROOT`
   - template directories that include the root `templates/` folder
   - Channels settings such as `ASGI_APPLICATION = "VideoWebsite.asgi.application"` and `CHANNEL_LAYERS`
   - `SCRIPTURE_API_URL` for the Bible API service
   - TinyMCE/CKEditor configuration if rich text editors are enabled

4. Apply migrations.

   ```bash
   python manage.py migrate
   ```

5. Optionally load the sample fixture.

   ```bash
   python manage.py loaddata data.json
   ```

6. Run the development server.

   ```bash
   python manage.py runserver
   ```

For WebSockets in development, run the ASGI app with Daphne if needed:

```bash
daphne VideoWebsite.asgi:application
```

## Data and External Services

The `connect` app talks to an external Scripture/Bible API through `connect/services.py`. The service currently contains a hard-coded API key; that should be moved into environment-backed settings before sharing or deploying the app.

The included `data.json` fixture contains development data, including a user record and sample social content. Treat it as local/demo data, not production seed data.

## Development Notes

- Tests exist as app-level `tests.py` files, but they are currently placeholders.
- Migrations are committed and should be preserved unless intentionally resetting app history.
- Uploaded media should stay out of git. Runtime upload folders such as `media/`, `uploads/`, `videos/`, `postimages/`, `audio_files/`, `podcast_picture/`, and `profile_pictures/` are ignored.
- `VideoWebsite/settings.py` is intentionally ignored for local secrets. Keep a documented example settings file if you recreate it for team use.
- The app packages and URL namespaces use `connect` and `groups`.
