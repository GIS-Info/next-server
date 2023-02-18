from rest_framework import serializers
from app.models import UserInfo


# User Serializer
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserInfo
        fields = (
        'id', 'username', 'email', 'is_superuser', 'first_name', 'last_name', 'email', 'is_staff', 'is_active')


# Register Serializer
class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserInfo
        fields = ('id', 'username', 'first_name', 'last_name', 'email', 'password')
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = UserInfo.objects.create_user(validated_data['username'], validated_data['email'], validated_data['password'])

        return user
