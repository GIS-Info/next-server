from rest_framework import serializers
from .models import GISource


class GISourceSerializer(serializers.ModelSerializer):
    class Meta:
        model = GISource
        fields = "__all__"
