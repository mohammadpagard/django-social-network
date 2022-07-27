from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from .models import Post
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import PostCreateUpdateForm
from django.utils.text import slugify


class PostDetailView(View):
    def get(self, request, post_id, post_slug):
        post = get_object_or_404(Post, pk=post_id, slug=post_slug)
        return render(request, 'post/post_detail.html', {'post': post})


class PostDeleteView(LoginRequiredMixin, View):
    def get(self, request, post_id):
        post = get_object_or_404(Post, pk=post_id)
        if request.user.id == post.user.id:
            post.delete()
            messages.success(request, 'Post deleted', 'success')
        else:
            messages.error(request, 'You can not delete post', 'danger')
        return redirect('home:home')


class PostUpdateView(LoginRequiredMixin, View):
    form_class = PostCreateUpdateForm

    def setup(self, request, *args, **kwargs):
        self.post_instance = get_object_or_404(Post, pk=kwargs['post_id'])
        return super().setup(request, *args, **kwargs)

    def dispatch(self, request, *args, **kwargs):
        post = self.post_instance
        if request.user.id != post.user.id:
            messages.error(request, 'You can not update this post', 'danger')
            return redirect('home:home')
        return super().dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        post = self.post_instance
        form = self.form_class(instance=post)
        return render(request, 'post/post_update.html', {'form': form})

    def post(self, request, *args, **kwargs):
        post = self.post_instance
        form = self.form_class(request.POST, instance=post)
        if form.is_valid():
            post_update = form.save(commit=False)
            post_update.slug = slugify(form.cleaned_data['body'][:50])
            post_update.save()
            messages.success(request, 'This post updated', 'success')
            return redirect('post:detail', post.id, post.slug)


class PostCreateView(LoginRequiredMixin, View):
    form_class = PostCreateUpdateForm

    def get(self, request, *args, **kwargs):
        form = self.form_class
        return render(request, 'post/post_create.html', {'form': form})

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            new_post = form.save(commit=False)
            new_post.slug = slugify(form.cleaned_data['body'][:50])
            new_post.user = request.user
            new_post.save()
            messages.success(request, 'Post just created successfully', 'success')
            return redirect('home:home')
