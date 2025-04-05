from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _
from django.db import models


class User(AbstractUser):
    email = models.EmailField(_("email address"), unique=True, blank=False)
    first_name = models.CharField(_("first name"), max_length=50, blank=False)
    last_name = models.CharField(_("last name"), max_length=50, blank=False)

    class Meta(AbstractUser.Meta):
        swappable = "AUTH_USER_MODEL"

    def __str__(self):
        return self.username
