from django.contrib import admin
import json
from django.core.serializers.json import DjangoJSONEncoder
from django.db.models import Count
from django.db.models.functions import TruncDay
from rangefilter.filter import DateRangeFilter, DateTimeRangeFilter
from django.core import serializers
# Register your models here.

from  .models import DHT22


class DHT22Admin(admin.ModelAdmin):

    list_display = ('temp', 'humidity', 'time')
    list_filter = ( ('time', DateTimeRangeFilter),)
    search_fields = ['time']
    
    
    def changelist_view(self, request, extra_context=None):
        # Aggregate new subscribers per day
        chart_data = DHT22.objects.all()
            
        
        as_json = serializers.serialize('json', list(chart_data))
        extra_context = extra_context or {"chart_data": as_json}
        
        return super().changelist_view(request, extra_context=extra_context)
    
admin . site . register ( DHT22 , DHT22Admin)