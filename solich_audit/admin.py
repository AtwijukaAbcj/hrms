"""
admin.py
"""

from django.contrib import admin

from solich_audit.models import AuditTag, SolichAuditInfo, SolichAuditLog

# Register your models here.

admin.site.register(AuditTag)
