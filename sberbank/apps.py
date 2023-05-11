from django.apps import AppConfig as BaseAppConfig
from django.utils.translation import gettext_lazy as _


class AppConfig(BaseAppConfig):
    name = 'sberbank'
    verbose_name = _('sberbank')
