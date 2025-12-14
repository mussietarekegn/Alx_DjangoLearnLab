from rest_framework import serializers
from django.contrib.auth import authenticate, get_user_model
from rest_framework.authtoken.models import Token
from .models import User

User = get_user_model()  

class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ("username", "email", "password", "bio")

    def create(self, validated_data):
        # Use get_user_model().objects.create_user
        user = User.objects.create_user(
            username=validated_data["username"],
            email=validated_data.get("email"),
            password=validated_data["password"],
            bio=validated_data.get("bio", "")
        )
        Token.objects.create(user=user)
        return user
    
class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        user = authenticate(
            username=data["username"],
            password=data["password"]
        )

        if not user:
            raise serializers.ValidationError("Invalid credentials")

        token, _ = Token.objects.get_or_create(user=user)

        return {
            "user": user,
            "token": token.key
        }

class UserProfileSerializer(serializers.ModelSerializer):
    followers_count = serializers.IntegerField(
        source="followers.count",
        read_only=True
    )

    class Meta:
        model = User
        fields = (
            "username",
            "email",
            "bio",
            "profile_picture",
            "followers_count",
        )
