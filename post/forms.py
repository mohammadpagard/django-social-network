from cProfile import label
from django import forms
from .models import Post, Comment


class PostCreateUpdateForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ('body',)

        widgets = {'body': forms.Textarea(
            attrs={'class': 'form-control'}
        )}


class CommentCreateForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('body',)

        widgets = {'body': forms.Textarea(
            attrs={'class': 'form-control'}
        )}


class CommentReplyForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('body',)

        widgets = {'body': forms.TextInput(
            attrs={
                'class': 'form-control p-4'
            }
        )}


class PostSearchForm(forms.Form):
    search = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
