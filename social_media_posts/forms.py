from django import forms

from social_media_posts.models import Post, PostComment


class AddPostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ('title', 'body')


class EditPostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ('title', 'body')


class PostCommentForm(forms.ModelForm):
    class Meta:
        model = PostComment
        fields = ("body",)
        widgets = {
            "body": forms.Textarea(attrs={"class": "form-control", "placeholder": "نظر خود را وارد کنید"})
        }


class AddReplyForm(forms.ModelForm):
    class Meta:
        model = PostComment
        fields = ("body",)
