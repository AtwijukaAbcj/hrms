"""
Admin registration for the solich_theme app
"""

from django.contrib import admin

from solich_theme.models import CompanyTheme, SolichColorTheme

# Register your solich_theme models here.
admin.site.register(SolichColorTheme)
admin.site.register(CompanyTheme)
