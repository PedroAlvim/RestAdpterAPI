from rest_framework import serializers

from .models import University


class UniversitySerializer(serializers.HyperlinkedModelSerializer):
    name = serializers.CharField(max_length=132)
    country = serializers.CharField(max_length=32)
    alpha_two_code = serializers.CharField(max_length=2)
    state_province = serializers.CharField(max_length=32, allow_blank=True, required=False)
    domains = serializers.StringRelatedField(many=True)
    web_pages = serializers.StringRelatedField(many=True)

    # domain
    # web_pages

    class Meta:
        model = University
        fields = ('id', 'name', 'country', 'alpha_two_code', 'state_province', 'domains', 'web_pages')
