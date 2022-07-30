from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse


class Post(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='posts')
    body = models.TextField()
    slug = models.SlugField()
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ('-created',)

    def __str__(self):
        return self.slug

    def get_absolute_url(self):
        return reverse('post:detail', args=(self.id, self.slug))

    def likes_count(self):
        return self.plike.count()

    # validation for like
    def user_like(self, user):
        user_like = user.ulike.filter(post=self)
        if user_like.exists():
            return True
        return False


class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='ucomment')
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='pcomment')
    reply = models.ForeignKey('self', on_delete=models.CASCADE, related_name='rcomment', blank=True, null=True)
    is_reply = models.BooleanField(default=False)
    body = models.TextField(max_length=300)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user} - {self.post}"


class Like(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='ulike')
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='plike')

    def __str__(self):
        return f"{self.user} liked {self.post.slug}"
    