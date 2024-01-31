from django import forms

from blogs.models import Blog
from mailing.forms import StyleFormMixin


class BlogForm(StyleFormMixin, forms.ModelForm):
    class Meta:
        model = Blog
        fields = ('title', 'body', 'image', 'date_of_creation', 'views_count', 'user',)
