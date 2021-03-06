# Filters model

import django_filters 
from django_filters import DateFilter, CharFilter
from .models import *

# filter on the orders
class OrderFilter(django_filters.FilterSet):

    start_date = DateFilter(label='Start date', field_name='date_created',lookup_expr='gte', input_formats=['%d-%m-%Y',])
    end_date = DateFilter(label='End date', field_name='date_created',lookup_expr='lte', input_formats=['%d-%m-%Y',])
    notes = CharFilter(label='Notes',field_name='notes',lookup_expr='icontains')

    class Meta:
        model = Order
        fields = '__all__'
        # Exlude fields
        exclude = ['customer','date_created']
