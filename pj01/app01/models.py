from django.db import models
import  datetime
from  django.utils  import  timezone
# Create your models here.

class DHT22 (models.Model):
    temp = models . DecimalField(max_digits=4, decimal_places=2)
    humidity = models . DecimalField(max_digits=4, decimal_places=2)
    time  =  models . DateTimeField ( blank=True )
    def  __str__ ( self ): 
        temp=str(self.temp)
        humidity=str(self.humidity)
        time=str(self.time)
        return  temp,humidity,time
    class Meta:
        ordering = ['-time']
    