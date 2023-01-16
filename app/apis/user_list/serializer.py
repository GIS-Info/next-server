from rest_framework import serializers
from django.contrib.auth.hashers import make_password
from app.models import UserInfo


class UserListSerializer(serializers.ModelSerializer):
    password = serializers.CharField(
        write_only=True,
        required=True,
    )

    class Meta:
        model = UserInfo
        fields = ['username', 'password', 'email', 'mobile']

    def create(self, validated_data):
        validated_data['password'] = make_password(validated_data.get('password'))
        return super().create(validated_data)

    def update(self, instance, validated_data):
        validated_data['password'] = make_password(validated_data.get('password'))
        return super().update(instance, validated_data)
