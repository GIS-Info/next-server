from rest_framework import serializers
from .models import GISource, NewUniversity,Cities, Countries


class GISourceSerializer(serializers.ModelSerializer):
    class Meta:
        model = GISource
        fields = "__all__"

class UniversitySerializer(serializers.ModelSerializer):
    class Meta:
        model = NewUniversity
        fields = "__all__"

class CitySerializer(serializers.ModelSerializer):
    class Meta:
        model = Cities
        fields = "__all__"

class CountrySerializer(serializers.ModelSerializer):
    class Meta:
        model = Countries
        fields = "__all__"


class UniCitySerializer(serializers.Serializer):
    id = serializers.IntegerField()
    University_Name_CN = serializers.CharField()
    University_Name_EN = serializers.CharField()
    University_Name_Local = serializers.CharField()
    URL = serializers.CharField()
    University_Abbr = serializers.CharField()
    University_Other_Name = serializers.CharField()
    Description_EN = serializers.CharField()
    City = serializers.CharField()
    Country = serializers.CharField()
    Description_CN = serializers.CharField()
    Unit_EN = serializers.CharField()
    Unit_CN = serializers.CharField()