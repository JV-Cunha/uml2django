import uuid

from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.utils.translation import gettext_lazy as _

from rest_framework_simplejwt.tokens import RefreshToken

from custom_auth.models.WebUserManager import WebUserManager


class WebUser(AbstractBaseUser, PermissionsMixin):
    # pk = models.UUIDField( SHOULD BE PK instead of uuid?
    id = models.UUIDField(
        primary_key=True, blank=False, default=uuid.uuid4,
        editable=False, unique=True,
    )
    email = models.EmailField(unique=True, null=False, blank=False)

    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=False)
    date_joined = models.DateTimeField(auto_now_add=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = WebUserManager()

    def __str__(self):
        return self.email

    @property
    def tokens(self):
        """Allow us to get a user's token by calling `user.token`."""
        refresh = RefreshToken.for_user(self)
        return {'refresh': str(refresh), 'access': str(refresh.access_token)}
