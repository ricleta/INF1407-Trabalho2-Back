from rest_framework import serializers
from .models import ReviewModel
from django.contrib.auth.models import User
from Games.serializers import GamesModelSerializer
from Games.models import GamesModel

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username']

class ReviewModelSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    # Use PrimaryKeyRelatedField for write operations (expects a game ID)
    game_id = serializers.PrimaryKeyRelatedField(queryset=GamesModel.objects.all(), source='game', write_only=True)
    # Use the nested GamesModelSerializer for read operations (shows full game details)
    game = GamesModelSerializer(read_only=True) 

    class Meta:
        model = ReviewModel
        fields = ['id', 'user', 'game', 'game_id', 'rating', 'comment', 'created_at']