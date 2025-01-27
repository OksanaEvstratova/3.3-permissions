import contextvars

from django_filters import rest_framework as filters

from advertisements.models import Advertisement


class AdvertisementFilter(filters.FilterSet):
    """Фильтры для объявлений."""

    created_at = filters.DateFromToRangeFilter()
    status = filters.CharFilter()

    class Meta:
        model = Advertisement
        fields = {
            'created_at': ['exact'],
            'status': ['exact', 'contains'],
        }

