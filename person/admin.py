from django.contrib import admin

# Register your models here.
from django.contrib import admin
from person.models import *

# Register your models here.
admin.site.register(Category)
admin.site.register(Post)
admin.site.register(video)
admin.site.register(Comments)
admin.site.register(CommentsVideos)
admin.site.register(Image)
admin.site.register(BlogPost)
# admin.site.register(Board)
admin.site.register(BoardImage)
admin.site.register(BoardVideo)
admin.site.register(BoardPost)
admin.site.register(BoardBlogPost)


# admin.site.register(Message)
# class ProfileAdmin(admin.ModelAdmin):
#     def save_related(self, request, form, formsets, add):
#         try:
#             super().save_related(request, form, formsets, add)
#         except Exception as e:
#             if 'no such table' in str(e):
#                 # Handle the missing table gracefully
#                 # e.g., display a user-friendly message, log the error, or skip saving the related data
#                 messages.error(request, "There was an issue saving the profile data.")
#             else:
#                 raise e
#
class BoardImageInline(admin.TabularInline):
    model = BoardImage
    extra = 1
    fields = ('image', 'order')
    ordering = ('order',)

class BoardVideoInline(admin.TabularInline):
    model = BoardVideo
    extra = 1
    fields = ('video', 'order')
    ordering = ('order',)

class BoardPostInline(admin.TabularInline):
    model = BoardPost
    extra = 1
    fields = ('post', 'order')
    ordering = ('order',)

class BoardBlogPostInline(admin.TabularInline):
    model = BoardBlogPost
    extra = 1
    fields = ('blog', 'order')
    ordering = ('order',)

class BoardAdmin(admin.ModelAdmin):
    inlines = [BoardImageInline, BoardVideoInline, BoardPostInline, BoardBlogPostInline]
    list_display = ('title', 'user', 'privacy')

admin.site.register(Board, BoardAdmin)
