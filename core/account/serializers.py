from rest_framework import serializers
from dj_rest_auth.registration.serializers import RegisterSerializer
from .models import User


class CustomRegisterSerializer(RegisterSerializer):
    """
    Custom serializer for registration to handle required 'first_name' and 'last_name' fields.
    """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Set _has_phone_field to False to bypass allauth's phone number logic
        self._has_phone_field = False
    
    username = serializers.CharField(max_length=150, required=True)
    first_name = serializers.CharField(max_length=150, required=True)
    last_name = serializers.CharField(max_length=150, required=True)

    def get_cleaned_data(self):
        """Add first_name and last_name to the cleaned_data for allauth."""
        data = super().get_cleaned_data()
        data['first_name'] = self.validated_data.get('first_name', '')
        data['last_name'] = self.validated_data.get('last_name', '')
        return data


class CustomUserDetailsSerializer(serializers.ModelSerializer):
    """
    Serializer for the User model to control which fields are returned.
    """

    class Meta:
        model = User
        fields = ("pk", "email", "username", "first_name", "last_name")
        read_only_fields = ("pk", "email")