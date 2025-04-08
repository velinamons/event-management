import django_filters
from .models import Event


class EventFilter(django_filters.FilterSet):
    organizer = django_filters.CharFilter(field_name='organizer__username', lookup_expr='icontains', label='Organizer (Username)')
    organizer_email = django_filters.CharFilter(field_name='organizer__email', lookup_expr='icontains', label='Organizer (Email)')

    title = django_filters.CharFilter(field_name='title', lookup_expr='icontains', label='Title')

    location = django_filters.CharFilter(field_name='location', lookup_expr='icontains', label='Location')

    date = django_filters.DateFilter(field_name='date', lookup_expr='icontains', label='Event Date')

    class Meta:
        model = Event
        fields = ['organizer', 'organizer_email', 'title', 'location', 'date']
