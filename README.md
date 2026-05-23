# Social Media App

A Django social media project for faith-centered community, media sharing, Bible reading, groups, and real-time messaging. The application is built as a traditional server-rendered Django site with multiple domain apps: user profiles, posts and media, direct/group chat, group and church communities, Bible content, search, playlists, and blogs.

The project is organized around the actual app package names `connect` and `groups`. The `connect` app owns Bible API integration and Bible data models; the `groups` app owns groups, church groups, memberships, group requests, and events.

## Current Status

This repository contains the Django project package, app code, templates, migrations, a sample fixture (`data.json`), and dependency pins. One required runtime file is intentionally not committed:

- `VideoWebsite/settings.py`

`manage.py`, `VideoWebsite/asgi.py`, and `VideoWebsite/wsgi.py` all expect `DJANGO_SETTINGS_MODULE=VideoWebsite.settings`, so a local settings module must be restored or recreated before running the app.

The Bible API key has been moved out of source code. `connect/services.py` now reads the key from environment-backed configuration through `SCRIPTURE_API_KEY`, with `bible_api_key` still supported as a legacy/local alias.

## Feature Overview

### Accounts and Profiles

Users can sign up, log in, update profile details, upload profile pictures, follow other users, block users, and view their own activity history. Profile pages aggregate a user's prayers, videos, images, blogs, saved content, boards, followers, and following relationships.

### Social Content

The `person` app contains the main social publishing system. Users can create rich-text prayers/posts, upload videos and images, create podcasts, publish blog-style posts, comment, like, view, save, and control visibility with privacy options such as public, followers-only, and private.

### Boards and Playlists

Boards let users collect and order mixed content, including images, videos, prayers, and blog posts. Playlists provide ordered collections of videos through `PlaylistItem`, supporting user-owned video curation.

### Groups and Church Groups

The `groups` app supports public/private groups, church groups, memberships, admin/member roles, join privacy, group creation requests, church creation requests, and group events. Group members can create group posts, prayers, images, and videos when allowed by the group's posting rules.

### Chat and Notifications

The `chat` app supports direct messages, chat rooms, group chat participants, unread message tracking, notification views, and WebSocket consumers through Django Channels. Notifications are created through `django-notifications-hq` for social actions such as follows, comments, new content, saves, and messages.

### Bible Connection

The `connect` app models Bible versions, books, chapters, and verses. It can fetch Bible data from an external Scripture API, render Bible lists/books/chapters, and seed local Bible content through management commands. API credentials are expected to come from local environment variables, not committed source code.

### Search and Recommendations

The `search` app searches across users, prayers, blog posts, videos, images, categories, and tags. Recommendation helpers use TF-IDF and cosine similarity from scikit-learn to find similar videos, images, posts, and blog posts based on titles, descriptions, tags, and rich text content.

## Tech Stack

- Python and Django 4.2
- Django Channels and Daphne for ASGI/WebSockets
- Redis support through `channels-redis`
- SQLite for simple local development, with `psycopg2-binary` available for PostgreSQL
- TinyMCE/CKEditor packages for rich text editing
- `django-notifications-hq` for in-app notifications
- `requests` and `python-dotenv` for external API access and local environment loading
- scikit-learn, TensorFlow/Keras, BeautifulSoup, NumPy, and related packages for similarity/search helpers
- Bootstrap packages and Django templates for the server-rendered UI

## Repository Layout

```text
VideoWebsite/     Project URL routing plus ASGI/WSGI entry points
user/             Authentication, profiles, follows, blocking, and profile dashboards
person/           Core social content: prayers, posts, images, videos, podcasts, boards, comments, recommendations
chat/             Direct messages, chat rooms, notification views, and WebSocket consumers
groups/           Groups, church groups, memberships, join requests, group content, and events
connect/          Bible versions, books, chapters, verses, API services, and seed commands
blog/             Separate simple blog app with CRUD views
playlistapp/      Video playlists and ordered playlist items
search/           Cross-content search view and template
templates/        Shared site templates such as base, index, login, signup, logout
data.json         Sample/development fixture data
requirements.txt  Python dependency list
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

## Configuration

Create a local `.env` file for secrets and local-only values. At minimum, Bible API usage expects:

```env
SCRIPTURE_API_KEY=replace-me
SCRIPTURE_API_URL=https://api.scripture.api.bible/v1/
```

`connect/services.py` also supports `bible_api_key` as a legacy alias for the API key. Prefer `SCRIPTURE_API_KEY` for new local setups.

Your uncommitted `VideoWebsite/settings.py` should provide at least:

- `SECRET_KEY`, `DEBUG`, and `ALLOWED_HOSTS`
- `INSTALLED_APPS` entries for this repo's Django apps and the third-party apps used in `requirements.txt`
- database configuration
- `STATIC_URL`, `STATIC_ROOT`, `MEDIA_URL`, and `MEDIA_ROOT`
- template directories that include the root `templates/` folder
- Channels settings such as `ASGI_APPLICATION = "VideoWebsite.asgi.application"` and `CHANNEL_LAYERS`
- `SCRIPTURE_API_URL` for the Bible API base URL
- TinyMCE/CKEditor configuration if rich text editors are enabled

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

3. Restore or create `VideoWebsite/settings.py`, then add your local `.env` values.

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

## Management Commands

- `python manage.py seed_data` fetches Bible books and chapters for configured Bible versions.
- `python manage.py verses` fetches verse-level data.
- `python manage.py create_fake_users` creates fake user accounts for local testing and requires the `Faker` package.

## Data Notes

The included `data.json` fixture contains development/demo data, including users, content, categories, notifications, and sample social activity. Treat it as local seed data only. It should not be treated as production data.

Uploaded media should stay out of git. Runtime upload folders such as `media/`, `uploads/`, `videos/`, `postimages/`, `audio_files/`, `podcast_picture/`, and `profile_pictures/` are ignored.

## Development Notes

- Tests exist as app-level `tests.py` files, but most are placeholders.
- Migrations are committed and should be preserved unless intentionally resetting app history.
- The app packages and URL namespaces use `connect` and `groups`.
- `VideoWebsite/settings.py` is intentionally ignored for local secrets. Keep a documented example settings file if you recreate it for team use.
- Keep API keys and service credentials in `.env` or local settings, not in committed source code.
