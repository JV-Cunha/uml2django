
from rest_framework.exceptions import ValidationError

from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from custom_auth.rest_api.serializers import (
    WebUserSignupSerializer,
)


class SignupAPIView(APIView):
    permission_classes = (AllowAny,)
    serializer_class = WebUserSignupSerializer

    def post(self, request: Request) -> Response:
        """Return user response after a successful registration."""
        user_request = request.data
        if 'password_confirmation' not in request.data.keys():
            raise ValidationError(
                {'password_confirmation': 'Inform password confirmation'}
            )
        if request.data['password'] != request.data['password_confirmation']:
            raise ValidationError(
                {'password_confirmation': ['Passwords did not match']})
        serializer = self.serializer_class(data=user_request)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
