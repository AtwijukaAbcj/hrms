from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class SolichAuthConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "solich_auth"
    verbose_name = _("Solich Auth")
