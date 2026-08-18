"""Solich ``AppLauncher`` for the database-backed template app."""

from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class SolichDBTemplateConfig(AppConfig):
    """Solich app config: registers ``solich_dbtemplate`` and auto-imports signal handlers."""

    default = True

    name = "solich_dbtemplate"
    verbose_name = _("Database Templates")
    default_auto_field = "django.db.models.BigAutoField"

    def ready(self):
        from . import signals

        return super().ready()
