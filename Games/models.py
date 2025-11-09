from django.db import models

class GamesModel(models.Model):
    '''
    Model representing a game.
    '''

    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=100, help_text='Título do jogo')
    platforms = models.CharField(max_length=100, help_text='Plataformas suportadas')
    description = models.TextField(max_length=500, help_text='Descrição do jogo')
    release_date = models.DateField(help_text='Data de lançamento')
    developer = models.ForeignKey('auth.User', on_delete=models.CASCADE)

    def formatted_platforms(self):
        # The platforms are saved as a string representation of a list, e.g., "['PC', 'Xbox']"
        return self.platforms.replace("[", "").replace("]", "").replace("'", "")

    def __str__(self):
        return self.title