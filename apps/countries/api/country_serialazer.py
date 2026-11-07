from rest_framework import serializers
from apps.countries.models import Country


FLAG_URL = "https://flagcdn.com/w320/{iso}.png"


class CountrySerializer(serializers.ModelSerializer):
    flag_url = serializers.SerializerMethodField()

    class Meta:
        model = Country
        fields = ["id", "name", "capital", "region", "iso_code", "flag_url"]

    def get_flag_url(self, obj):
        return FLAG_URL.format(iso=obj.iso_code.lower())
