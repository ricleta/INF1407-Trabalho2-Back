from django import forms
from .models import GamesModel

class GamesForm(forms.ModelForm):
    """
    Form for creating and updating Games instances.

    This form defines the fields and validation rules for the Games model.
    """

    platforms = forms.MultipleChoiceField(
        choices=[
            ('PC', 'PC'),
            ('PlayStation', 'PlayStation'),
            ('Xbox', 'Xbox'),
            ('Nintendo Switch', 'Nintendo Switch'),
            ('Mobile', 'Mobile'),
            ('Wii', 'Wii'),
        ],
        widget=forms.CheckboxSelectMultiple,
        help_text='Selecione as plataformas em que o jogo está disponível',
        label='Plataformas'
    )

    class Meta:
        model = GamesModel
        fields = ['title', 'platforms', 'description', 'release_date']
        error_messages = {
                'title': {
                    'required': "O título é obrigatório.",
                    'max_length': "O título não pode ter mais de 100 caracteres.",
                },
                'platforms': {
                    'required': "As plataformas são obrigatórias.",
                    'max_length': "As plataformas não podem ter mais de 100 caracteres.",
                },
                'description': {
                    'required': "A descrição é obrigatória.",
                    'max_length': "A descrição não pode ter mais de 500 caracteres.",
                },
                'release_date': {
                    'required': "A data de lançamento é obrigatória.",
                    'invalid': "Por favor, insira uma data válida.",
                }
            }

    def clean_title(self):
        """
        Custom validation for the 'title' field.

        Ensures that the title is not empty and has a minimum length of 3 characters.
        """
        title = self.cleaned_data.get('title')
        if title is None:
            raise forms.ValidationError("O título é obrigatório.")
        elif len(title) <= 3:
            raise forms.ValidationError("O título deve ter no mínimo 3 caracteres.")
        return title

    def clean_description(self):
        """
        Custom validation for the 'description' field.

        Ensures that the description is not empty and has a minimum length of 20 characters.
        """
        description = self.cleaned_data.get('description')
        if description is None:
            raise forms.ValidationError("A descrição é obrigatória.")
        elif len(description) <= 20:
            raise forms.ValidationError("A descrição deve ter no mínimo 20 caracteres.")
        return description