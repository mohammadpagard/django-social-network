from django.contrib import admin
from .models import Post, Comment


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('user', 'slug', 'updated')
    search_fields = ('body', 'slug')
    list_filter = ('updated', 'user')
    prepopulated_fields = {'slug': ('body',)}
    raw_id_fields = ('user',)


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('user', 'post', 'created', 'is_reply')
    search_fields = ('post', 'user')
    list_filter = ('created', 'user', 'reply')
    raw_id_fields = ('user', 'post', 'reply')
