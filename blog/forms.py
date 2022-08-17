from django.forms import ModelForm, widgets
from django import forms
from .models import Post

class PostForm(ModelForm):
    class Meta:
        model = Post
        # fields = '__all__'
        fields = [
            'title',
            'text',
            'image',
            'tags'
        ]
        labels = {
            'title': 'Tytuł',
            'text': 'Treść',
            'image': 'Zdjęcie',
            'tags': 'Tagi',
        }
        widgets = {
            'tags': forms.SelectMultiple(),
        }

    def __init__(self, *args, **kwargs):
        super(PostForm, self).__init__(*args, **kwargs)

        self.fields['title'].widget.attrs.update({'class': 'form-control'})
        self.fields['title'].widget.attrs.update({'placeholder': 'Tytuł'})

        self.fields['text'].widget.attrs.update({'class': 'form-control'})
        self.fields['text'].widget.attrs.update({'placeholder': 'Treść'})

        self.fields['tags'].widget.attrs.update({'class': 'form-control'})

        self.fields['image'].widget.attrs.update({'class': 'form-control-file'})
