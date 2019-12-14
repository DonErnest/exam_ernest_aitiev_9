from django.contrib import admin

# Register your models here.
from webapp.models import Photo, Comment, Like


class PhotoAdmin(admin.ModelAdmin):
    list_display = ['id', 'photo', 'description', 'author', 'likes', 'created_at']
    list_display_links = ['id', 'description']
    list_filter = ['author']
    search_fields = ['description', 'author']
    fields = ['photo', 'description', 'author', 'likes', 'created_at']
    readonly_fields = ['created_at']

class CommentAdmin(admin.ModelAdmin):
    list_display = ['id', 'text', 'photo', 'author', 'added']
    list_display_links = ['id', 'text']
    list_filter = ['author', 'photo']
    search_fields = ['text', 'author']
    fields = ['text', 'photo', 'author', 'added']
    readonly_fields = ['added']

admin.site.register(Photo, PhotoAdmin)
admin.site.register(Comment, CommentAdmin)
admin.site.register(Like)