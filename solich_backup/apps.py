from django.apps import AppConfig


class BackupConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "solich_backup"

    def ready(self):
        from django.urls import include, path

        from solich.urls import urlpatterns

        urlpatterns.append(
            path("backup/", include("solich_backup.urls")),
        )
        super().ready()
