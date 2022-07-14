from django.contrib.auth import authenticate

from rest_framework.serializers import (
    ModelSerializer, SerializerMethodField,
    EmailField, CharField
)
from rest_framework.exceptions import ValidationError

from custom_auth.models import WebUser


class WebUserLoginSerializer(ModelSerializer):
    email = EmailField()
    password = CharField(max_length=128, write_only=True)
    tokens = SerializerMethodField()

    class Meta:
        model = WebUser
        fields = ("email", "password", "tokens")

    def validate(self, data):  # type: ignore
        """Validate and return user login."""
        email = data.get('email', None)
        password = data.get('password', None)
        if email is None:
            raise ValidationError('An email address is required to login.')

        if password is None:
            raise ValidationError('A password is required to login.')

        user = authenticate(email=email, password=password)
        webuser = WebUser.objects.get(email=email)
        if webuser:
            if not webuser.is_active:
                raise ValidationError('This user is not currently activated.')

        if user is None:
            raise ValidationError({'password': ['Wrong password']})

        return user

    def get_tokens(self, obj):  # type: ignore
        """Get user token."""
        webuser = obj
        return {
            'refresh': webuser.tokens['refresh'],
            'access': webuser.tokens['access']
        }
