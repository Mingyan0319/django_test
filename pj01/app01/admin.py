from django.contrib import admin
from django.contrib.admin.views.main import ChangeList
from django.core import serializers
from django.urls import path
from django.http import HttpResponse
 
from rangefilter.filter import DateTimeRangeFilter
 
from .models import DHT22
 
class TimeChangeList(ChangeList):
    def get_results(self, request):
        super().get_results(request)
        self.chart_data = serializers.serialize('json', list(self.result_list.all()))
 
class DHT22Admin(admin.ModelAdmin):
    list_display = ('temp', 'humidity', 'time')
    list_filter = (('time', DateTimeRangeFilter), )
    search_fields = ['time']
    __ajax_get_chart_data_path = 'chart_data/'
 
    def changelist_view(self, request, extra_context=None):
        extra_context = extra_context or {'ajax_get_chart_data_path': self.__ajax_get_chart_data_path}
 
        return super().changelist_view(request, extra_context=extra_context)
 
    def get_urls(self):
        urls = super().get_urls()
        extra_urls = [
            path(self.__ajax_get_chart_data_path, self.admin_site.admin_view(self.__ajax_get_chart_data))
        ]
        return extra_urls + urls
 
    def get_changelist(self, request):
        return TimeChangeList
 
    def __ajax_get_chart_data(self, request):
        cl = self.get_changelist_instance(request)
        cl.get_results(request)
        return HttpResponse(cl.chart_data)
 
admin.site.register(DHT22, DHT22Admin)
