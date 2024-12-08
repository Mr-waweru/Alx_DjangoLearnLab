from django import forms
from .models import Post, Comment

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ["title", "content"]

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
