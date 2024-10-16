from rest_framework import serializers
from .models import MovieReview

class ReviewSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source= 'user.username', read_only=True)
    class Meta:
        model = MovieReview
        fields = ['id', 'title', 'review_content', 'rating', 'username', 'created']
        read_only_fields = ['user', 'created']

    def validate_rating(self, value):
        if value < 1 or value > 5:
            raise serializers.ValidationError("Rating must be between 1 and 5")
        return value
    
    def create(self, validate_data):
        return MovieReview.objects.create(user=self.context['request'].user, **validate_data)