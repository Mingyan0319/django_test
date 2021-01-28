from django.contrib import admin
import json
from django.core.serializers.json import DjangoJSONEncoder
from django.db.models import Count
from django.db.models.functions import TruncDay
from rangefilter.filter import DateRangeFilter, DateTimeRangeFilter
from django.core import serializers
from django.http import JsonResponse
from django.urls import path
# Register your models here.

from  .models import DHT22


class DHT22Admin(admin.ModelAdmin):

    list_display = ('temp', 'humidity', 'time')
    list_filter = ( ('time', DateTimeRangeFilter),)
    search_fields = ['time']
    
    
    def changelist_view(self, request, extra_context=None):
        # Aggregate new subscribers per day
        chart_data = self.chart_data()
           
        as_json = serializers.serialize('json', list(chart_data))
        extra_context = extra_context or {"chart_data": as_json}
        
        return super().changelist_view(request, extra_context=extra_context)
    
    def get_urls(self):
        urls = super().get_urls()
        extra_urls = [
            path("chart_data/", self.admin_site.admin_view(self.chart_data_endpoint))
        ]
        # NOTE! Our custom urls have to go before the default urls, because they
        # default ones match anything.
        return extra_urls + urls
    
    def chart_data_endpoint(self, request):
        chart_data = self.chart_data()
        return JsonResponse(list(chart_data), safe=False)

    def chart_data(self):
        return (
            DHT22.objects.all()
        )
    
admin . site . register ( DHT22 , DHT22Admin)
