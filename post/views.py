from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from .models import Post, Comment, Like
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import PostCreateUpdateForm, CommentCreateForm, CommentReplyForm
from django.utils.text import slugify
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator


class PostDetailView(View):
    form_class = CommentCreateForm
    form_class_reply = CommentReplyForm

    def setup(self, request, *args, **kwargs):
        self.post_instance = get_object_or_404(Post, pk=kwargs['post_id'], slug=kwargs['post_slug'])
        return super().setup(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        comment = self.post_instance.pcomment.filter(is_reply=False)
        # if user liked this post, so button is disabled.(validation for likes)
        user_like = False
        if request.user.is_authenticated and self.post_instance.user_like(request.user):
            user_like = True

        return render(request, 'post/post_detail.html', {
            'post': self.post_instance,
            'comment': comment,
            'form': self.form_class,
            'reply_form': self.form_class_reply,
            'user_like': user_like
        })

    @method_decorator(login_required)
    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            new_comment = form.save(commit=False)
            new_comment.user = request.user
            new_comment.post = self.post_instance
            new_comment.save()
            messages.success(request, "You're comment has been successfully registered", 'success')
            return redirect('post:detail', self.post_instance.id, self.post_instance.slug)


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


class PostReplyView(LoginRequiredMixin, View):
    form_class = CommentReplyForm

    def post(self, request, *args, **kwargs):
        post = get_object_or_404(Post, id=kwargs['post_id'])
        comment = get_object_or_404(Comment, id=kwargs['comment_id'])
        form = self.form_class(request.POST)
        if form.is_valid():
            reply = form.save(commit=False)
            reply.user = request.user
            reply.post = post
            reply.reply = comment
            reply.is_reply = True
            reply.save()
            messages.success(request, "You're reply comment has been successfully registered", 'success')
        return redirect('post:detail', post.id, post.slug)


class PostLikeView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        post = get_object_or_404(Post, id=kwargs['post_id'])
        like = Like.objects.filter(post=post, user=request.user)
        if like.exists():
            messages.error(request, 'You already liked this post!', 'danger')
        else:
            Like.objects.create(post=post, user=request.user)
            messages.success(request, 'You liked this post.', 'success')
        return redirect('post:detail', post.id, post.slug)
