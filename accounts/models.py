from __future__ import unicode_literals

import uuid
from datetime import datetime

from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.core.mail import send_mail
from django.db import models
from django.utils.translation import gettext_lazy as _
from parler.models import TranslatableModel

from .managers import UserManager


class User(AbstractBaseUser, PermissionsMixin):
    id = models.AutoField(primary_key=True, editable=False, unique=True)
    unique_id = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    email = models.EmailField(_("email"), blank=True)
    phone = models.BigIntegerField(unique=True, null=False)
    first_name = models.CharField(_("name"), max_length=50, blank=True)
    last_name = models.CharField(_("surname"), max_length=50, blank=True)
    middle_name = models.CharField(_("middle_name"), max_length=60, blank=True)
    date_joined = models.DateTimeField(_("registered"), auto_now_add=True)
    is_active = models.BooleanField(_("is_active"), default=True)
    updated_on = models.DateTimeField(auto_now=True)
    is_superuser = models.BooleanField(default=False)
    is_staff = models.BooleanField(_("staff status"), default=False)
    user_image = models.ImageField(upload_to="staticfiles/img/profile", default="/static/img/image.png")
    distribution = models.BooleanField(default=False, blank=False)
    admin = models.BooleanField(null=True)
    force_logout_date = models.DateTimeField(null=True, blank=True)
    rassilka = models.BooleanField(default=True, null=True, blank=True)


    objects = UserManager()

    USERNAME_FIELD = "phone"
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = _("user")
        verbose_name_plural = _("users")

    def force_logout(self):
        self.force_logout_date = datetime.now()
        self.save()

    def get_full_name(self):
        full_name = f"{self.last_name} {self.first_name} {self.middle_name}"
        return full_name

    def get_short_name(self):
        return self.first_name

    def email_user(self, subject, message, from_email=None, **kwargs):
        send_mail(subject, message, from_email, [self.email], **kwargs)

    def about(self):
        data = {
            "id": self.id,
            "phone": self.phone
        }
        return data

    def __str__(self):
        return f'{self.phone} - {self.last_name}'


class Confirm_phone(models.Model):
    phone = models.BigIntegerField(null=False, blank=False)
    code = models.IntegerField(null=False, unique=True)
    confirm_phone = models.BooleanField(default=False)
    ucaller_id = models.IntegerField(default=0)


class Agreement(TranslatableModel):
    id = models.AutoField(primary_key=True, editable=False, unique=True)
    title = models.TextField(_("Глава"))
    text = models.TextField(_("Текст"))


    def __str__(self):
        return self.title

