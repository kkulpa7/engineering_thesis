from django.forms import ModelForm
from django import forms
from .models import Pigeon

class PigeonForm(ModelForm):
    class Meta:
        model = Pigeon
        # fields = '__all__'
        fields = [
            'number',
            'color',
            'gender',

            'name',
            'birth_date',
            'mother',
            'father',
            'description',
            'status',

            'image_body',
            'image_wing',
            'image_eye',
        ]
        labels = {
            'number': 'Number obrączki',
            'color': 'Kolor',
            'gender': 'Płeć',
            'name': 'Nazwa',
            'birth_date': 'Data wyklucia',
            'mother': 'Matka',
            'father': 'Ojciec',
            'description': 'Opis',
            'status': 'Status',

            'image_body': 'Zdjęcie gołębia',
            'image_wing': 'Zdjęcie skrzydła',
            'image_eye': 'Zdjęcie oka',
        }

    def __init__(self, *args, **kwargs):
        super(PigeonForm, self).__init__(*args, **kwargs)

        for name, field in self.fields.items():
            if name.find('image') != -1:
                field.widget.attrs.update({'class': 'form-control-file'})
            else:
                field.widget.attrs.update({'class': 'form-control'})
        # self.fields['gender'].widget.attrs.update({'class': 'form-control'})
