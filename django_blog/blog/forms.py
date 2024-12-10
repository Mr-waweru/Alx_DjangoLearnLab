from django import forms
from .models import Post, Comment
from taggit.forms import TagField, TagWidget


class PostForm(forms.ModelForm):
    tags = TagField(required=False)

    class Meta:
        model = Post
        fields = ["title", "content", "tags"]  # Include 'tags' in the fields list
        widgets = {
            "title": forms.TextInput(attrs={"class": "form-control"}),
            "content": forms.Textarea(attrs={"class": "form-control", "rows": 5}),
            "tags": TagWidget(attrs={"class": "form-control", "placeholder": "Add tags separated by commas"}),  # Use TagWidget
        }

    def save(self, commit=True):
        post = super().save(commit=False)
        # Additional custom logic, if needed
        if commit:
            post.save()
            self.save_m2m()  # Save many-to-many relationships, such as tags
        return post


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ["content"]  # Only include the content field
        widgets = {
            "content": forms.Textarea(
                attrs={"class": "form-control", "placeholder": "Add a comment...", "rows": 3}
            ),
        }
