from django.db import models
from django.contrib.auth.models import User
from Games.models import GamesModel

class ReviewModel(models.Model):
    '''
    Model representing a game review.
    '''
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, help_text='Usuário que criou a avaliação')
    game = models.ForeignKey(GamesModel, on_delete=models.CASCADE, help_text='Jogo que está sendo avaliado', related_name='reviews', default=None)
    rating = models.IntegerField(help_text='Nota de 1 a 10')
    comment = models.TextField(max_length=500, help_text='Comentário sobre o jogo')
    created_at = models.DateTimeField(auto_now_add=True, help_text='Data de criação')

    class Meta:
        unique_together = [['user', 'game']]

    def __str__(self):
        return f"{self.game.title} ({self.rating}) - {self.user.username}"
