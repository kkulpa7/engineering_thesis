from django.forms import ModelForm, widgets
from django import forms
from .models import Post, Comment


class PostForm(ModelForm):
    class Meta:
        model = Post
        # fields = '__all__'
        fields = [
            'title',
            'text',
            'tags',
        ]
        labels = {
            'title': 'Tytuł',
            'text': 'Treść',
            'tags': 'Tagi',
        }
        # widgets = {
        #     'tags': forms.SelectMultiple(),
        # }

    def __init__(self, *args, **kwargs):
        super(PostForm, self).__init__(*args, **kwargs)

        for name, field in self.fields.items():
            field.widget.attrs.update({'class': 'form-control'})
            field.widget.attrs.update({'placeholder': field.label})

        self.fields['tags'].widget.attrs.update({'data-role': 'tagsinput'})
    # self.fields['title'].widget.attrs.update({'placeholder': 'Tytuł'})
    #
    # self.fields['text'].widget.attrs.update({'class': 'form-control'})
    # self.fields['text'].widget.attrs.update({'placeholder': 'Treść'})
    #
    # self.fields['tags'].widget.attrs.update({'class': 'form-control'})


class CommentForm(ModelForm):
    class Meta:
        model = Comment
        fields = [
            'value',
            'text'
        ]
        labels = {
            'value': 'Typ',
            'text': 'Treść',
        }

    def __init__(self, *args, **kwargs):
        super(CommentForm, self).__init__(*args, **kwargs)

        for name, field in self.fields.items():
            field.widget.attrs.update({'class': 'form-control'})
            field.widget.attrs.update({'placeholder': field.label})
