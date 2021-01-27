from django.shortcuts import render
# Create your views here.
from django.views.generic import TemplateView
from chartjs.views.lines import BaseLineChartView

from datetime import datetime
from django.http import HttpResponse
import Adafruit_DHT
from .models import DHT22
from .filters import DHT22Filter
from plotly.offline import plot
import plotly.graph_objs as go


def index(request):
    return render(request, 'app01/index.html')


def sayhi1(request):
    now = datetime.now()
    html = "<html><body>Hello World <br>Django test. %s.</body></html>" % now
    return HttpResponse(html)

def dht22(request):
    now = datetime.today()
    sensor = Adafruit_DHT.DHT22
    pin = 4
    humidity, temperature = Adafruit_DHT.read_retry(sensor, pin)
    temp = 'Temperature:{0:0.1f} humidity:{1:0.1f}'.format(temperature, humidity)
    time = 'Time:%s'%now
    return HttpResponse('<hl>'+temp+'<br>'+time)
def hello(request):
    return render(request, 'hello.html', {
        'current_time': str(datetime.now()),
    })

class LineChartJSONView(BaseLineChartView):
    def get_labels(self):
        """Return 7 labels for the x-axis."""
        return ["January", "February", "March", "April", "May", "June", "July"]

    def get_providers(self):
        """Return names of datasets."""
        return ["Central", "Eastside", "Westside"]

    def get_data(self):
        """Return 3 datasets to plot."""

        return [[75, 44, 92, 11, 44, 95, 35],
                [41, 92, 18, 3, 73, 87, 92],
                [87, 21, 94, 3, 90, 13, 65]]


line_chart = TemplateView.as_view(template_name='line_chart.html')
line_chart_json = LineChartJSONView.as_view()