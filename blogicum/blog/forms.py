from django import forms
from django.contrib.auth import get_user_model
from django.utils import timezone

from .models import Comment, Post

User = get_user_model()


class PostForm(forms.ModelForm):
    """Форма публикации."""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['pub_date'].initial = timezone.localtime(
            timezone.now()
        ).strftime('%Y-%m-%dT%H:%M')

    class Meta:
        model = Post
        exclude = ('author', 'is_published')
        widgets = {
            'pub_date': forms.DateTimeInput(
                format='%Y-%m-%dT%H', attrs={'type': 'datetime-local'}
            ),
        }


class CommentForm(forms.ModelForm):
    """Форма для комментариев"""

    class Meta:
        model = Comment
        fields = ('text',)


class ProfileForm(forms.ModelForm):

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'username', 'email')
