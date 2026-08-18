"""
solich_automations/filters.py
"""

from solich.filters import SolichFilterSet, django_filters
from solich_automations.models import MailAutomation


class AutomationFilter(SolichFilterSet):
    """
    AutomationFilter
    """

    search = django_filters.CharFilter(field_name="title", lookup_expr="icontains")

    class Meta:
        model = MailAutomation
        fields = "__all__"
