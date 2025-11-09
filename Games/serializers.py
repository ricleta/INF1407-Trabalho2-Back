from rest_framework import serializers
from .models import GamesModel

class GamesModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = GamesModel
        fields = '__all__'