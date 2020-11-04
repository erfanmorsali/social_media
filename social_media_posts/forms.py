from django import forms

from social_media_posts.models import Post


class AddPostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ('title', 'body')


class EditPostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ('title', 'body')