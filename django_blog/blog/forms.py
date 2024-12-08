from django import forms
from .models import Post

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
