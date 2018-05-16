from django import forms

from .models import Post, Category
from taggit.forms import TagWidget

class PostForm(forms.ModelForm):
   
    class Meta:
        model = Post
        fields = ('title', 'category' ,'description')

        labels = {
            'category': 'Category',
        }

        widgets = {
                'category': TagWidget()
        }

class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ('name',)
