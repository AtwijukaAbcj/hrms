from django.contrib import admin

from solich_automations.models import MailAutomation

# Register your models here.


admin.site.register(
    [
        MailAutomation,
    ]
)
