# Filters model

import django_filters 
from django_filters import DateFilter, CharFilter
from .models import *

# filter on the orders
class OrderFilter(django_filters.FilterSet):
    start_date = DateFilter(field_name='date_created',lookup_expr='gte')
    end_date = DateFilter(field_name='date_created',lookup_expr='lte')
    notes = CharFilter(field_name='notes',lookup_expr='icontains')

    class Meta:
        model = Order
        fields = '__all__'
        # Exlude fields
        exclude = ['customer','date_created']