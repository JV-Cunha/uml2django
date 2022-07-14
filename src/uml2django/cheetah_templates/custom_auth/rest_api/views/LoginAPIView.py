from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.serializers import EmailField

from custom_auth.rest_api.serializers import (
    WebUserLoginSerializer,
)

class LoginAPIView(APIView):

    permission_classes = (AllowAny,)
    serializer_class = WebUserLoginSerializer

    def post(self, request: Request) -> Response:
        """Return user after login."""
        user = request.data

        serializer = self.serializer_class(data=user)
        if not serializer.is_valid():
            print(serializer.errors)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        return Response(serializer.data, status=status.HTTP_200_OK)