from django.shortcuts import render, redirect
from django.views import View
from .models import Post


class PostDetailView(View):
    def get(self, request, post_id, post_slug):
        post = Post.objects.get(pk=post_id, slug=post_slug)
        return render(request, 'post/post_detail.html', {'post': post})
