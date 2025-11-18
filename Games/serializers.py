from rest_framework import serializers
from .models import GamesModel

from rest_framework import serializers
from django.contrib.auth.models import User # Import the User model
from .models import GamesModel

# This serializer will represent the User object in a nested way.
class DeveloperSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username'] # We only need the username

class GamesModelSerializer(serializers.ModelSerializer):
    # Tell the developer field to use the nested serializer.
    # It's read-only because it's populated based on the authenticated user who creates the game.
    developer = DeveloperSerializer(read_only=True)

    class Meta:
        model = GamesModel
        fields = ['id', 'title', 'platforms', 'description', 'release_date', 'developer']
