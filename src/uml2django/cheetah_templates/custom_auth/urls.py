from django.urls import path

from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView, TokenVerifyView

from custom_auth.rest_api.views.SignupAPIView import SignupAPIView
from custom_auth.rest_api.views.LoginAPIView import LoginAPIView



urlpatterns = [
    path("signup", SignupAPIView.as_view(), name="auth-signup"),
    path("login", LoginAPIView.as_view(), name="auth-signup"),
    path('token', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh', TokenRefreshView.as_view(), name='token_refresh'),
    path('token/verify', TokenVerifyView.as_view(), name='token_verify'),
]
