from django import forms
from .models import Post, Comment
from taggit.forms import TagField

class PostForm(forms.ModelForm):
    tags = TagField(required=False)

    class Meta:
        model = Post
        fields = ["title", "content"]
        widgets = {
            "title": forms.TextInput(attrs={"class": "form-control"}),
            "content": forms.Textarea(attrs={"class": "form-control", "rows": 5}),
        }

    def save(self, commit=True):
        post = super().save(commit=False)
        # Additional custom logic, if needed
        if commit:
            post.save()
        return post


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ["content"]  # Only include the content field
        widgets = {
            "content": forms.Textarea(attrs={"class": "form-control", "placeholder": "Add a comment...", "rows": 3}),
        }
