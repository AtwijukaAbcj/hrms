from django.apps import AppConfig
from django.conf import settings


class SolichMeetConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "solich_meet"
    verbose_name = "Meet"

    def ready(self):
        from django.urls import include, path

        from solich.urls import urlpatterns
        from solich_meet import signals

        settings.APPS.append("solich_meet")

        urlpatterns.append(
            path("meet/", include("solich_meet.urls")),
        )
        super().ready()
