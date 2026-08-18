"""
Shared Django test helpers for Solich unit tests.

Prefer these factories over copying setUp boilerplate across apps.
"""

from solich.testkit.company import CompanyFilterTestMixin, clear_selected_company
from solich.testkit.factories import make_company, make_employee, make_user

__all__ = [
    "CompanyFilterTestMixin",
    "clear_selected_company",
    "make_company",
    "make_employee",
    "make_user",
]
