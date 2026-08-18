import django_filters

from solich.filters import SolichFilterSet
from whatsapp.models import WhatsappCredientials


class CredentialsViewFilter(SolichFilterSet):
    search = django_filters.CharFilter(
        field_name="meta_phone_number", lookup_expr="icontains"
    )

    class Meta:
        model = WhatsappCredientials
        fields = ["meta_phone_number", "search"]
