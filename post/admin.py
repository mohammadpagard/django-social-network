from django.contrib import admin
from .models import Post, Comment, Like
from autosave.mixins import AdminAutoSaveMixin


@admin.register(Post)
class PostAdmin(AdminAutoSaveMixin, admin.ModelAdmin):
    list_display = ('user', 'title', 'updated')
    search_fields = ('body', 'title')
    list_filter = ('updated', 'user')
    prepopulated_fields = {'slug': ('body',)}
    raw_id_fields = ('user',)
    autosave_last_modified_field = "updated"


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('user', 'post', 'created', 'is_reply')
    search_fields = ('post', 'user')
    list_filter = ('created', 'user', 'reply')
    raw_id_fields = ('user', 'post', 'reply')


@admin.register(Like)
class LikeAdmin(admin.ModelAdmin):
    list_filter = ('user',)
