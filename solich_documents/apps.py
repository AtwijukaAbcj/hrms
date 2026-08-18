from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class SolichDoumentsConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "solich_documents"
    verbose_name = _("Documents")
