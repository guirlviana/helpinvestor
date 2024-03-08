from rest_framework import serializers

class InvestorSerializer(serializers.Serializer):
    name = serializers.CharField(required=True, allow_blank=False, max_length=30)
    last_name = serializers.CharField(required=True, allow_blank=False, max_length=30)
    email = serializers.EmailField(required=True, allow_blank=False)
    password = serializers.CharField(required=True, allow_blank=False, max_length=30)
    phone = serializers.CharField(required=True, allow_blank=False, max_length=30)

    def validate_phone(self, value):
        if not value:
            raise serializers.ValidationError("Phone cannot be empty")

        cleaned_value = value.lstrip('+')
        if not cleaned_value.isdigit():
            raise serializers.ValidationError("Phone must contain only numeric characters and may have a leading '+'")

        return value