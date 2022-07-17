from rest_framework import serializers

from accounts.serializers import UserSerializer

from reviews.models import Review

class ReviewSerializer(serializers.ModelSerializer):

    class Meta:
        model  = Review
        fields = "__all__"
        depth  = 1