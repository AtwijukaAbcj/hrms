from django.apps import AppConfig


class SolichWidgetsConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "solich_widgets"

    def ready(self):
        from solich_widgets.widgets.file_widgets import patch_clearable_file_input

        patch_clearable_file_input()
