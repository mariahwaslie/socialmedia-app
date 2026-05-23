# from django.shortcuts import render
# from django.views.generic import TemplateView
# from django.db.models import Q
# from django.contrib.auth.models import User
#
# import user.models
# from person.models import BlogPost, Post, video, Image, Podcast, Catagory,Boards
# from user.models import Profile
# import blog.models
# import connect.models
# # from django.contrib.postgres.search import SearchVector, SearchQuery, SearchRank
# from bs4 import BeautifulSoup
# from django.http import HttpResponse
#
# # class Search(TemplateView):
# #     template_name = 'search.html'
# def search_in_html(content, query):
#     soup = BeautifulSoup(content, 'html.parser')
#     return query.lower() in soup.get_text().lower()
#
# def search(request,search=" "):
#     query = request.GET.get('search', '')
#
#         # Fetch user profile if authenticated
#     if request.user.is_authenticated:
#         profile = (Profile.objects
#                                   .filter(user=request.user)
#                                   .values('bio', 'profile_picture').first())
#     else:
#         profile= None
#
#         # Search users by username, first name, and last name
#     users = User.objects.filter(Q(username__icontains=query) |
#                                     Q(first_name__icontains=query) |
#                                     Q(last_name__icontains=query))
#     users_search = User.objects.filter(username=query)
#
#
#
#     blog_posts = [post for post in BlogPost.objects.all() if search_in_html(post.content, query)]
#     posts = [post for post in Post.objects.all() if search_in_html(post.content, query)]
#     blogs = [post for post in blog.models.Post.objects.all() if search_in_html(post.content, query)]
#     bible_chapter_content= [chapter for chapter in connect.models.Chapter.objects.filter(bibleversion__versionid='f72b840c855f362c-04')
#                                 if search_in_html(chapter.content, query)]
#     bible_chapter_name = [chapter for chapter in connect.models.Chapter.objects.filter(bibleversion__versionid='f72b840c855f362c-04')
#                                 if search_in_html(chapter.name, query)]
#     bible_book_name = [chapter for chapter in
#                            connect.models.Chapter.objects.filter(bibleversion__versionid='f72b840c855f362c-04')
#                            if search_in_html(chapter.book.name, query)]
#
#
#
#         # Search other models
#     tags = video.objects.filter(tags__name__icontains=query )
#     videos = video.objects.filter(Q(title__icontains=query) | Q(description__icontains=query))
#     image_titles = Image.objects.filter(title__icontains=query)
#     image_descriptions = Image.objects.filter(description__icontains=query)
#     image_tags = Image.objects.filter(tags_img__name__icontains=query)
#
#
#
#     boards= Boards.objects.filter(Q(title__icontains=query,privacy='public') |
#                                   Q(title__icontains=query, privacy='only_me', user=request.user)|
#                                   Q(description__icontains=query, privacy='public') |
#                                   Q(description__icontains=query, privacy='only_me', user=request.user)|
#                                   Q(images__title__icontains=query,privacy='public', user=request.user)|
#                                   Q(videos__title__icontains=query,privacy='public', user=request.user)|
#                                   Q(posts__title__icontains=query,privacy='public', user=request.user)|
#                                   Q(blogs__title__icontains=query,privacy='public', user=request.user)|
#                                   Q(images__tags__name__icontains=query,privacy='public', user=request.user)|
#                                   Q(videos__tags__name__icontains=query, privacy='public', user=request.user) |
#                                   Q(posts__tags__name__icontains=query, privacy='public', user=request.user) |
#                                   Q(blogs__tags__name__icontains=query, privacy='public', user=request.user) |
#                                   Q(images__description__icontains=query, privacy='public', user=request.user) |
#                                   Q(videos__description__icontains=query, privacy='public', user=request.user) |
#                                   Q(posts__content__icontains=query, privacy='public', user=request.user) |
#                                   Q(blogs__content__icontains=query, privacy='public', user=request.user) )
#
#
#         # Search podcasts
#     audios = Podcast.objects.filter(Q(title__icontains=query) | Q(description__icontains=query))
#         # Aggregate results
#     results = ( list(blog_posts) + list(posts) +list(blogs)+
#                 list(videos) + list(tags) + list(image_titles) + list(image_descriptions) +
#                 list(image_tags) + list(audios) + list(bible_chapter_content)+list(bible_chapter_name)
#                 +list(bible_book_name))
#     results = list(set(results))
#     context={
#             'blog_posts': blog_posts,
#             'posts':  list(set(posts)),
#             'users': list(set(users) | set(users_search)),
#             'query': query,
#             'results': list(set(results)),
#             'videos': list(set(videos) | set(tags)),
#             'images': image_titles,
#             'blogs':list(set(blog_posts)),
#             'usernames':users_search,
#             'categories':Catagory.objects.all(),
#             'bible_ch': list(set(bible_chapter_content)),
#             'bible_ch_name':list(set(bible_chapter_name)),
#             'bible_books': list(bible_book_name),
#             'profile':Profile.objects.all(),
#             'boards':list(set(boards)),
#             # 'user_follows': request.user.following.all()
#         } # Remove duplicates
#     return render(request, 'search.html', context)
from django.shortcuts import render
from django.views.generic import TemplateView
from django.db.models import Q
from django.contrib.auth.models import User
import user.models
from person.models import BlogPost, Post, video, Image, Podcast, Category, Board
from user.models import Profile
import blog.models
import connect.models
# from django.contrib.postgres.search import SearchVector, SearchQuery, SearchRank
from bs4 import BeautifulSoup
from django.http import HttpResponse



# class Search(TemplateView):
#     template_name = 'search.html'
def search_in_html(content, query):
    soup = BeautifulSoup(content, 'html.parser')
    return query.lower() in soup.get_text().lower()


def search(request, search=" "):
    query = request.GET.get('search', '')

    # Fetch user profile if authenticated
    if request.user.is_authenticated:
        profile = (Profile.objects
                   .filter(user=request.user)
                   .values('bio', 'profile_picture').first())
    else:
        profile = None

    # search_results = SearchQuerySet().filter(content=query)

    # Search users by username, first name, and last name
    users = User.objects.filter(Q(username__icontains=query) |
                                Q(first_name__icontains=query) |
                                Q(last_name__icontains=query) |
                                Q(username=query))
    # users_search = User.objects.filter(username=query)

    blog_posts = []
    for post in BlogPost.objects.all():
        if search_in_html(post.content, query) or search_in_html(post.title, query):
            blog_posts.append(post)
    posts = []
    for post in Post.objects.all():
        if search_in_html(post.content, query) or search_in_html(post.title, query):
            posts.append(post)

    blogs = []
    for post in blog.models.Post.objects.all():
        if search_in_html(post.content, query) or search_in_html(post.title, query):
            blogs.append(post)

    # bible_chapter_content=[]
    # for chapter in connect.models.Chapter.objects.filter(bibleversion__versionid='f72b840c855f362c-04'):
    #      if search_in_html(chapter.content, query) or search_in_html(chapter.content, query):
    #          bible_chapter_content.append(chapter)

    # bible_chapter_name = [chapter for chapter in connect.models.Chapter.objects.filter(bibleversion__versionid='f72b840c855f362c-04')
    #                             if search_in_html(chapter.name, query)]

    # Search other models
    videos = video.objects.filter(
        Q(tags__name__icontains=query) | Q(title__icontains=query) | Q(description__icontains=query))
    images = Image.objects.filter(
        Q(title__icontains=query) | Q(description__icontains=query) | Q(tags_img__name__icontains=query))

    # if request.user.is_authenticated:
    #     boards= Boards.objects.filter(Q(title__icontains=query,privacy='public') |
    #                                 Q(title__icontains=query, privacy='only_me', user=request.user)|
    #                                 Q(description__icontains=query, privacy='public') |
    #                                 Q(description__icontains=query, privacy='only_me', user=request.user)|
    #                                 Q(images__title__icontains=query,privacy='public', user=request.user)|
    #                                 Q(videos__title__icontains=query,privacy='public', user=request.user)|
    #                                 Q(posts__title__icontains=query,privacy='public', user=request.user)|
    #                                 Q(blogs__title__icontains=query,privacy='public', user=request.user)|
    #                                 Q(images__tags__name__icontains=query,privacy='public', user=request.user)|
    #                                 Q(videos__tags__name__icontains=query, privacy='public', user=request.user) |
    #                                 Q(posts__tags__name__icontains=query, privacy='public', user=request.user) |
    #                                 Q(blogs__tags__name__icontains=query, privacy='public', user=request.user) |
    #                                 Q(images__description__icontains=query, privacy='public', user=request.user) |
    #                                 Q(videos__description__icontains=query, privacy='public', user=request.user) |
    #                                 Q(posts__content__icontains=query, privacy='public', user=request.user) |
    #                                 Q(blogs__content__icontains=query, privacy='public', user=request.user) )
    # else:
    #     boards=None

    # Search podcasts
    # audios = Podcast.objects.filter(Q(title__icontains=query) | Q(description__icontains=query))
    # Aggregate results
    results = list(set(list(blog_posts) + list(posts) + list(blogs) +
                       list(videos) + list(images)))
    context = {
        'blog_posts': blog_posts,
        'posts': list(set(posts)),
        'users': list(set(users)),
        'query': query,
        'results': list(set(results)),
        'videos': list(set(videos)),
        'images': set(images),
        'blogs': list(set(blogs)),
        # 'usernames':users_search,
        'categories': Category.objects.all(),
        # 'bible_ch': list(set(bible_chapter_content)),
        # 'bible_ch_name':list(set(bible_chapter_name)),
        # 'bible_books': list(bible_book_name),
        'profile': Profile.objects.all(),
        # 'boards':boards,
        # 'user_follows': request.user.following.all()
    }  # Remove duplicates
    return render(request, 'search.html', context)
