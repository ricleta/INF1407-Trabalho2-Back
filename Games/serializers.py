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
    developer = DeveloperSerializer(read_only=True)
    
    # Add a field to explicitly fetch reviews
    reviews = serializers.SerializerMethodField()

    class Meta:
        model = GamesModel
        # Add 'reviews' to the list of fields
        fields = ['id', 'title', 'platforms', 'description', 'release_date', 'developer', 'reviews']

    def get_reviews(self, obj):
        # Fetch related reviews using the 'related_name="reviews"' defined in the ReviewModel
        reviews = obj.reviews.all()
        return [
            {
                "user": {"username": review.user.username},
                "rating": review.rating,
                "comment": review.comment
            }
            for review in reviews
        ]