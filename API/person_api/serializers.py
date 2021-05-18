from rest_framework import serializers

from .models import University


class DynamicFieldsModelSerializer(serializers.ModelSerializer):
    """
    A ModelSerializer that takes an additional `fields` argument that
    controls which fields should be displayed.
    """

    def __init__(self, *args, **kwargs):
        # Instantiate the superclass normally
        super(DynamicFieldsModelSerializer, self).__init__(*args, **kwargs)

        fields = self.context['request'].query_params.get('fields')
        print('request: ', self.context['request'].query_params)
        if fields:
            fields = fields.split(',')
            # Drop any fields that are not specified in the `fields` argument.

            allowed = set(fields)
            existing = set(self.fields.keys())
            for field_name in existing - allowed:
                self.fields.pop(field_name)


class UniversitySerializer(DynamicFieldsModelSerializer):
    domains = serializers.StringRelatedField(many=True)
    web_pages = serializers.StringRelatedField(many=True)

    class Meta:
        model = University
        fields = ['id', 'name', 'country', 'alpha_two_code', 'state_province', 'domains', 'web_pages']
