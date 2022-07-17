from django.contrib.auth.hashers import make_password
from rest_framework import serializers

from accounts.models import User


class UserSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)

    email = serializers.EmailField()
    first_name = serializers.CharField(max_length=60)
    last_name = serializers.CharField(max_length=60)
    password = serializers.CharField(max_length=128, write_only=True)

    date_joined = serializers.DateTimeField(read_only=True)
    updated_at = serializers.DateTimeField(read_only=True)

    def validate_email(self, email: str):
        email_exists = User.objects.filter(email=email).exists()

        if email_exists:
            raise ValueError({"email": ["email already exists."]}, 400)

        return email

    def create(self, validated_data):
        user = User.objects.create_staffuser(**validated_data)
        return user


class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField(source="username")
    password = serializers.CharField()