# Django packages
from django import forms
# Third pary apps
from ckeditor.widgets import CKEditorWidget
# Local apps
from .models import Post, Comment


class PostCreateUpdateForm(forms.ModelForm):
    body = forms.CharField(widget=CKEditorWidget())

    class Meta:
        model = Post
        fields = ('body', 'title')

        widgets = {'title': forms.TextInput(
            attrs={'class': 'form-control'}
        )}


# bio = forms.CharField(widget=CKEditorWidget(
#         attrs={'class': 'form-control'}
#     ))

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
