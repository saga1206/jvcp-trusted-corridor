from rest_framework import serializers
from .models import Provider, ProviderVerification, Review

class ReviewSerializer(serializers.ModelSerializer):
    author = serializers.ReadOnlyField(source='author.username')

    class Meta:
        model = Review
        fields = ['id', 'author', 'rating', 'comment', 'created_at']

class ProviderVerificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProviderVerification
        fields = ['id', 'status', 'certification_reference', 'submitted_at', 'reviewed_at']
        read_only_fields = ['status', 'submitted_at', 'reviewed_at']

class ProviderSerializer(serializers.ModelSerializer):
    reviews = ReviewSerializer(many=True, read_only=True)
    average_rating = serializers.SerializerMethodField()

    class Meta:
        model = Provider
        fields = ['id', 'name', 'category', 'description', 'location',
                  'languages_spoken', 'is_verified', 'reviews', 'average_rating', 'created_at']
        read_only_fields = ['is_verified']

    def get_average_rating(self, obj):
        reviews = obj.reviews.all()
        if not reviews:
            return None
        return round(sum(r.rating for r in reviews) / len(reviews), 1)