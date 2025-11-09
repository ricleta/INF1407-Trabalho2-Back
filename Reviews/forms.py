from .models import ReviewModel
from django import forms
from Games.models import GamesModel

class ReviewForm(forms.ModelForm):
    '''
    Form for creating and updating game reviews.
    '''
    game = forms.ModelChoiceField(
        queryset=GamesModel.objects.all(),
        label="Jogo",
        empty_label="Selecione um jogo",
        to_field_name="title"
    )

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)

        # If the form is bound to an existing instance (i.e. we are editing a review),
        # only allow the user to select the game they originally reviewed.
        if self.instance and self.instance.pk:
            self.fields['game'].queryset = GamesModel.objects.filter(pk=self.instance.game.pk)

    class Meta:
        model = ReviewModel
        fields = ['game', 'rating', 'comment']
        labels = {
            'game': 'Título do Jogo',
            'rating': 'Nota (1 a 10)',
            'comment': 'Comentário',
        }
        help_texts = {
            'game': 'Informe o título do jogo ou filme.',
            'rating': 'Escolha uma nota de 1 a 10.',
            'comment': 'Escreva um comentário sobre o jogo com (min. 20 | máx. 500) caracteres.',
        }
        error_messages = {
            'game': {'max_length': 'O título é muito longo.', 'required': 'O título é obrigatório.'},
            'rating': {'required': 'A nota é obrigatória.'},
            'comment': {'max_length': 'O comentário é muito longo.', 'required': 'O comentário é obrigatório.'},
        }

    def clean(self):
        """
        Custom validation to ensure a user doesn't review the same game twice.
        This check is only performed when creating a new review.
        """
        cleaned_data = super().clean()
        game = cleaned_data.get('game')

        # self.instance.pk is None for new reviews (CreateView)
        if self.instance.pk is None and game and self.user:
            if ReviewModel.objects.filter(user=self.user, game=game).exists():
                raise forms.ValidationError("Você já fez uma avaliação para este jogo.")

        return cleaned_data
    
    def clean_rating(self):
        """Custom validation to ensure rating is between 1 and 10."""
        rating = self.cleaned_data.get('rating')
        
        print(f"########## Rating is {rating} ##############")

        if rating is None:
            raise forms.ValidationError("A nota é obrigatória.")
        if rating < 1 or rating > 10:
            raise forms.ValidationError("A nota deve ser um número inteiro entre 1 e 10.")
        
        return rating

    def clean_comment(self):
        """Custom validation to ensure comment is valid."""
        comment = self.cleaned_data.get('comment')
        
        if not comment:
            raise forms.ValidationError("O comentário é obrigatório.")
        if len(comment) < 10:
            raise forms.ValidationError("O comentário deve ter pelo menos 10 caracteres.")
        if len(comment) > 500:
            raise forms.ValidationError("O comentário não pode exceder 500 caracteres.")
        
        return comment