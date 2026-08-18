"""
sap_integration/sidebar.py

Sidebar configuration for SAP Integration module
"""

from django.urls import reverse
from django.utils.translation import gettext_lazy as trans

MENU = trans("SAP Integration")
IMG_SRC = "images/ui/settings.svg"
ACCESSIBILITY = "sap_integration.sidebar.menu_accessibility"

SUBMENUS = [
    {
        "menu": trans("Dashboard"),
        "redirect": reverse("sap_integration:dashboard"),
        "accessibility": "sap_integration.sidebar.dashboard_accessibility",
    },
    {
        "menu": trans("Configuration"),
        "redirect": reverse("sap_integration:configure"),
        "accessibility": "sap_integration.sidebar.configure_accessibility",
    },
    {
        "menu": trans("Sync Logs"),
        "redirect": reverse("sap_integration:sync_logs"),
        "accessibility": "sap_integration.sidebar.sync_logs_accessibility",
    },
]


def menu_accessibility(request, menu, user_perms, *args, **kwargs):
    """
    Check if SAP Integration menu should be accessible to the user.
    Requires either superuser or SAP integration admin permission.
    """
    return request.user.is_superuser or request.user.has_perm(
        "sap_integration.view_sapintegrationconfig"
    )


def dashboard_accessibility(request, submenu, user_perms, *args, **kwargs):
    """
    Check if SAP Integration dashboard is accessible.
    """
    return request.user.is_superuser or request.user.has_perm(
        "sap_integration.view_sapintegrationconfig"
    )


def configure_accessibility(request, submenu, user_perms, *args, **kwargs):
    """
    Check if SAP configuration page is accessible.
    Requires change permission.
    """
    return request.user.is_superuser or request.user.has_perm(
        "sap_integration.change_sapintegrationconfig"
    )


def sync_logs_accessibility(request, submenu, user_perms, *args, **kwargs):
    """
    Check if sync logs page is accessible.
    Requires view permission.
    """
    return request.user.is_superuser or request.user.has_perm(
        "sap_integration.view_sapsynclog"
    )
