from django.contrib.auth.password_validation import validate_password

from rest_framework.serializers import ModelSerializer
from rest_framework.exceptions import ValidationError

from custom_auth.models import WebUser


class WebUserSignupSerializer(ModelSerializer):
    class Meta:
        model = WebUser
        fields = ("email", "password")
        extra_kwargs = {
            "password": {"write_only": True, 'required': True},
            "email": {'required': True}
        }

    def validate(self, data):
        # get the password from the data
        password = data.get('password')

        try:
            # validate the password and catch the exception
            validate_password(password=password)
        except Exception as e:
            raise ValidationError({'password': list(e.messages)})

        return super(WebUserSignupSerializer, self).validate(data)

    def create(self, validated_data):
        webuser = WebUser.objects.create_user(**validated_data)
        return webuser
