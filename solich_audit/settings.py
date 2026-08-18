"""
solich_audit/settings.py

This module is used to write settings contents related to payroll app
"""

from solich.settings import TEMPLATES

TEMPLATES[0]["OPTIONS"]["context_processors"].append(
    "solich_audit.context_processors.history_form",
)
