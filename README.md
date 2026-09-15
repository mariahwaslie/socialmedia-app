# social media platform

A full-stack Django social media application for community publishing, real-time messaging, reading, media sharing, groups, communities, events, playlists, boards, search, and content recommendations.

I built this project mainly on my own as a long-form software engineering project. The core application design, Django models, views, URL structure, feature work, data relationships, and integration decisions were built through my own implementation work.

This project started as a social media application, but it grew into a larger platform with multiple connected product areas. Users can create posts, upload videos and images, write blog-style content, follow or block people, join groups, request church communities, message other users, organize saved content, browse Bible content, and discover related posts through search and recommendation helpers.

## Project overview

The application is a traditional server-rendered Django project organized into several domain apps. Each app owns a different part of the product:

- `user` handles authentication, profile pages, profile editing, follows, blocking, and user dashboards.
- `person` is the main social content app. It handles prayer posts, videos, images, podcasts, blog-style posts, comments, likes, saves, boards, explore pages, and recommendation helpers.
- `chat` handles direct messages, chat rooms, group messages, unread state, notification views, and WebSocket consumers.
- `groups` handles public/private groups, church groups, memberships, join requests, creation requests, group content, posting permissions, and events.
- `connect` handles Bible versions, books, chapters, verses, Scripture API calls, and local Bible data seeding.
- `playlistapp` handles user-created video playlists with ordered playlist items.
- `blog` contains a standalone blog CRUD flow.
- `search` aggregates search across users, rich-text posts, blog posts, videos, images, tags, and categories.

The result is closer to a small social platform than a single-purpose Django app. A lot of the work went into making separate features talk to each other: group posts are still social posts, chat rooms can belong to groups, videos can belong to playlists and boards, users can save and organize content, and recommendation utilities compare content across multiple media types.

## Why I built it

I wanted to build something large enough to force real backend decisions. A basic tutorial app usually has one or two models and a small set of views. This project gave me practice with the kinds of problems that come up when an application grows:

- How to divide a Django project into apps without losing track of relationships between them
- How to model many-to-many relationships with extra data, such as ordered board and playlist items
- How to connect user actions to notifications
- How to support private, public, followers-only, member-only, and admin-only behavior
- How to add WebSocket communication to a mostly server-rendered Django app
- How to store local data fetched from an external API
- How to search and recommend content across different models
- How to keep media uploads, fixtures, static files, migrations, and environment variables organized

Each new feature introduced new relationships with the rest of the system, so the project became a practical exercise in maintaining a growing codebase.

## Development context

This was primarily a solo engineering project. I used AI tools in a limited way, mainly for debugging errors and helping with front-end layout or styling. The main backend implementation, model design, feature planning, Django routing, data relationships, and product flows were built by me.

That matters because this project reflects more than the final code. It reflects the process of learning how to build a multi-app Django project, diagnose framework issues, connect separate features, and keep going when the application became larger than the original idea.

## Engineering scope

This project includes:

- Custom Django models across eight application areas
- Authentication and profile management
- User follows, blocking, and profile dashboards
- Rich-text social posts
- Image, video, and audio upload workflows
- Blog-style publishing
- Likes, views, comments, saves, and activity history
- Ordered boards that can contain mixed content types
- Ordered video playlists
- Public/private group workflows
- Church group request and membership workflows
- Group-level permissions for posting
- Event creation and editing for groups
- Direct messaging and chat rooms
- WebSocket consumers for chat, notifications, comments, and upload status
- Notification creation through `django-notifications-hq`
- Bible API service methods
- Bible data models and seed commands
- Search across multiple content models
- Recommendation helpers using TF-IDF and cosine similarity
- Local fixture data for development
- Environment variable support through `.env.example`

## Main product areas

### Accounts and profiles

Users can sign up, log in, log out, and manage profile information. Profile data includes a bio, profile picture, followers, following relationships, and blocked users. The app also creates profile-related records automatically when a new Django `User` is created.

Profile pages are not just account pages. They act as dashboards where users can view their own posts, prayers, images, videos, blogs, history, followers, following lists, and saved or created content.

### Social publishing

The `person` app is the center of the social experience. Users can create several types of content:

- Prayer posts with rich text
- Uploaded videos
- Uploaded images
- Blog-style posts
- Podcasts with audio files and cover images

Content supports privacy controls, user ownership, timestamps, tags or categories, likes, views, saves, and comments. Many content types can also be connected to groups, which lets the same publishing system support both personal profiles and group communities.

### Comments, likes, saves, and views

The app tracks social engagement across several content types. Posts, images, videos, and blog posts have their own comment flows. Videos support threaded replies through parent comments. Likes, saves, and views are modeled with Django many-to-many relationships so each user action can be attached to the content item.

The project also includes notification behavior for social activity, so user actions can trigger in-app notifications.

### Boards

Boards let users organize mixed content in one place. A board can contain:

- Images
- Videos
- Prayer posts
- Blog posts

Each board relationship uses a through model with an `order` field. That made the feature more involved than a simple many-to-many relationship because the app needs to preserve the user's chosen order across different content types. There is also a dedicated route for reordering board items.

### Playlists

Playlists let users create ordered collections of videos. The playlist system uses a `PlaylistItem` through model so each video can have a position inside the playlist. Playlists also support privacy settings and tags.

### Groups

The `groups` app supports a community system with public and private groups. Users can browse groups, join groups, or request access when a group requires approval. Groups include membership roles, including member and admin, and the app stores join requests separately so they can be reviewed.

Groups also have posting rules. A group can allow all members to post, or restrict posting to admins. Group content can include posts, prayers, images, videos, and events.

### Church groups

The project includes a separate church group model in addition to the regular group model. Church groups support their own creation requests, membership records, member requests, admin/member roles, join privacy, posting rules, and parent/child relationships for small groups.

This made the group system larger than a simple "create group and join group" feature. It includes approval workflows, role-based behavior, and different community types.

### Events

Groups can create events with titles, rich-text descriptions, event dates, location type, organizer, and event type. Supported event types include conferences, webinars, workshops, seminars, meetups, and Bible studies.

Events are connected to groups, which gives the community features a calendar-like extension instead of limiting groups to static discussion pages.

### Chat and real-time messaging

The chat system supports both direct messages and chat rooms. The models separate individual messages, single chats, and chat rooms. Messages track sender, recipient, message body, date, and read state.

The real-time layer uses:

- Django Channels
- Daphne
- ASGI routing
- Redis channel layers
- WebSocket consumers
- Auth middleware for WebSocket connections

The app includes WebSocket consumers for direct chat and group chat. When a user sends a chat message, the app saves the message, sends it through the channel layer, and creates notifications for recipients.

### Notifications

Notifications are handled through `django-notifications-hq`. The app uses notifications for messaging and social actions such as follows, comments, new content, saves, and related user activity.

Users can view notifications and mark individual notifications as read.

### Bible reading and Scripture API integration

The `connect` app integrates Bible content into the social platform. It models:

- Bible versions
- Books
- Chapters
- Verses

The `BibleService` class handles Scripture API calls for Bible versions, books, chapters, chapter content, and verses. The project also includes custom Django management commands to seed Bible data into the local database.

This part of the app required thinking about external API access, local caching/storage, management commands, and how Bible content should fit into the rest of the platform.

### Search

The search app searches across multiple model types instead of just one table. It can search:

- Users
- Prayer posts
- Blog-style posts
- Standalone blog posts
- Videos
- Images
- Tags
- Categories

Because some content is stored as rich-text HTML, the search code uses BeautifulSoup to extract readable text before matching search terms.

### Recommendations

The project includes recommendation helpers for related content. The utilities use scikit-learn tools such as `TfidfVectorizer` and cosine similarity to compare text from titles, descriptions, tags, categories, and rich-text content.

Recommendation helpers compare across several content relationships:

- Similar videos to a video
- Similar images to an image
- Similar posts to a post
- Similar blog posts to a post
- Similar images or videos related to a post
- Similar posts related to an image or video

This was one of the more challenging parts of the project because the app has several content models, and each one stores searchable information differently.

## Architecture notes

### Server-rendered Django structure

The application uses Django templates rather than a separate JavaScript front end. Shared templates live in the root `templates/` directory, while app-specific templates live inside each app. Static CSS lives under `static/`, and collected/admin static files are present under `staticfiles/`.

### ASGI and WebSockets

The project uses `VideoWebsite/asgi.py` to combine regular HTTP handling with WebSocket routing. The ASGI application combines WebSocket URL patterns from both the `person` and `chat` apps.

Redis is configured as the Channels backend at `127.0.0.1:6379`, which allows WebSocket consumers to publish events to channel groups.

### Data modeling

The app uses Django's built-in `User` model and extends user behavior with profile, follow, and blocking models. Content models are split by type instead of forcing every post into one generic table. That made the project easier to reason about while building, because videos, images, blog posts, prayer posts, podcasts, boards, playlists, groups, and Bible content each have their own fields and relationships.

For ordered collections, the project uses through models:

- `BoardImage`
- `BoardVideo`
- `BoardPost`
- `BoardBlogPost`
- `PlaylistItem`

Those models preserve item order while still using Django many-to-many relationships.

### Privacy and permissions

The application includes several privacy and permission layers:

- Public content
- Followers-only content
- Only-me/private content
- Public and private groups
- Automatic or approval-based group joining
- Member or admin-only group posting
- User blocking
- Membership roles for groups and church groups

These choices affect what users can create, join, view, or interact with.

## Tech stack

- Python
- Django 4.2.15
- Django templates
- Bootstrap 5
- Custom CSS
- Django Channels
- Daphne
- Redis
- `channels-redis`
- SQLite for local development
- PostgreSQL support through `psycopg2-binary`
- TinyMCE
- CKEditor-related dependencies
- Django auth
- django-allauth dependencies/configuration
- `django-notifications-hq`
- scikit-learn
- NumPy
- BeautifulSoup
- TensorFlow/Keras dependencies
- Requests
- `python-dotenv`
- Faker

## Repository structure

```text
VideoWebsite/      Django project settings, URL routing, ASGI, and WSGI entry points
user/              Authentication views, profiles, follows, blocking, and profile dashboards
person/            Core social features: posts, media, blogs, boards, comments, recommendations
chat/              Direct messages, chat rooms, notifications, and WebSocket consumers
groups/            Groups, church groups, memberships, requests, permissions, and events
connect/           Bible API service layer, Bible data models, and seed commands
playlistapp/       Video playlists and ordered playlist items
blog/              Standalone blog CRUD flow
search/            Cross-content search view and search template
templates/         Shared templates such as base, index, login, signup, and logout
static/            Project CSS and static assets
staticfiles/       Collected/admin static assets
data.json          Local development fixture data
requirements.txt   Python dependency pins
```

## Important routes

| Area | Example routes |
| --- | --- |
| Auth and profile | `/signup/`, `/login/`, `/logout/`, `/profile/`, `/profile/update/` |
| Prayer posts | `/create/prayer/`, `/post/<user_id>/<post_id>/<action>/`, `/edit/prayer/<id>` |
| Media | `/uploadvideo/`, `/profile/createimage/`, `/video/<user_id>/<video_id>/<action>/`, `/image/<user_id>/<image_id>/<action>/` |
| Boards | `/createboard/`, `/viewboard/<username>/<board_id>`, `/board/<board_id>/reorder/` |
| Blogs | `/post/blogview/`, `/blogpost/<id>/<action>`, `/blog/post/new/` |
| Chat | `/chat/inbox/`, `/chat/messages/<username>`, `/chat/chatroom/<id>` |
| Groups | `/groups/groups/`, `/groups/request/group/`, `/groups/group/<id>`, `/groups/event/create/<group_id>` |
| Bible | `/bible/bibles/`, `/bible/books/<bible_id>`, `/bible/<bible_id>/<book>/chapter/<chapter_id>` |
| Playlists | `/playlist/create/`, `/playlist/<id>/`, `/playlist/<id>/add/` |
| Search | `/search/search/?search=<query>` |

## Local setup

### Prerequisites

- Python 3.10+
- Redis for WebSocket/channel-layer behavior
- A Scripture API key for Bible content features

### Installation

1. Clone the repository.

   ```bash
   git clone <your-repo-url>
   cd socialmedia-app
   ```

2. Create and activate a virtual environment.

   ```bash
   python -m venv .venv
   source .venv/bin/activate
   ```

3. Install dependencies.

   ```bash
   pip install -r requirements.txt
   ```

4. Create a local `.env` file.

   ```bash
   cp .env.example .env
   ```

5. Add local configuration values.

   ```env
   SECRET_KEY=replace-me
   DEBUG=True
   ALLOWED_HOSTS=localhost,127.0.0.1
   SCRIPTURE_API_URL=https://api.scripture.api.bible/v1/
   SCRIPTURE_API_KEY=replace-me
   TINYMCE_API_KEY=replace-me
   ```

6. Apply migrations.

   ```bash
   python manage.py migrate
   ```

7. Optionally load sample development data.

   ```bash
   python manage.py loaddata data.json
   ```

8. Run the development server.

   ```bash
   python manage.py runserver
   ```

For WebSocket behavior, make sure Redis is running locally and start the ASGI app with Daphne when needed:

```bash
daphne -b 127.0.0.1 -p 8000 VideoWebsite.asgi:application
```

## Management commands

```bash
python manage.py seed_data
python manage.py verses
python manage.py create_fake_users
```

- `seed_data` fetches Bible book and chapter data for configured Bible versions.
- `verses` fetches verse-level Bible data.
- `create_fake_users` creates local test users using Faker.

## Configuration and security notes

- Local development uses SQLite through the configured `mydatabase` database file.
- Redis is configured as the default Channels backend at `127.0.0.1:6379`.
- Runtime uploads are stored under the configured media directory and should not be committed.
- `.env.example` documents the expected local environment variables.
- Secrets and API keys should live in environment variables or hosting-provider secret management before deployment.
- Any API key that was ever committed should be rotated before the repository is made public.

## Data and media notes

The included `data.json` fixture is intended for local development and demos. It may include sample users, content, categories, notifications, and social activity.

Uploaded media directories such as `media/`, `uploads/`, `videos/`, `postimages/`, `audio_files/`, `podcast_picture/`, and `profile_pictures/` should stay out of version control.

## What this project shows

This project shows my ability to build beyond a small tutorial-style application. It includes a real set of connected product features, and it required me to work across backend architecture, user flows, data modeling, templates, WebSockets, external APIs, search, recommendation logic, and local development setup.

The strongest engineering parts of the project are:

- Designing a multi-app Django codebase
- Modeling complex relationships between users, content, communities, messages, and saved collections
- Building authenticated create/read/update/delete flows across many content types
- Adding real-time communication to a server-rendered app
- Connecting external API data to local Django models
- Implementing search across HTML-rich content and multiple model types
- Building recommendation utilities with Python machine learning libraries
- Managing migrations, fixtures, static assets, media uploads, and environment variables

## Planned improvements

- Expand automated test coverage beyond placeholder app test files
- Centralize duplicated recommendation utilities into a shared service module
- Move all deployable secrets and API keys fully into environment-backed settings
- Add CI checks for formatting, migrations, and Django system checks
- Add production deployment settings for PostgreSQL, static assets, allowed hosts, and secure cookies
- Improve search ranking and indexing for larger datasets
- Continue refining the front end for consistency across profile, group, search, and media pages
