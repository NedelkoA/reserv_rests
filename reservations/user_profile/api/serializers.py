from rest_framework import serializers
from django.contrib.auth.models import User

from ..models import UserProfile


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            'id',
            'username',
            'first_name',
            'last_name',
            'email',
            'date_joined',
        )


class UserProfileSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(
        default=serializers.CurrentUserDefault(),
        write_only=True
    )
    user_repr = UserSerializer(
        read_only=True,
        source='user'
    )

    class Meta:
        model = UserProfile
        fields = (
            'id',
            'user',
            'user_repr',
            'status_user',
            'telephone',
            'telegram_id',
        )


class CreateUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            'username',
            'password',
        )


class CreateUserProfileSerializer(serializers.ModelSerializer):
    user = CreateUserSerializer()

    class Meta:
        model = UserProfile
        fields = (
            'user',
            'status_user',
            'telephone',
            'telegram_id',
        )

    def create(self, validated_data):
        user = User.objects.create(
            username=validated_data['user']['username'],
            password=validated_data['user']['password']
        )

        profile = UserProfile.objects.create(
            user=user,
            telephone=validated_data['telephone']
        )

        return profile
