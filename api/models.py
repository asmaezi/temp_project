
from django.db import models

class SensorData(models.Model):
    temperature = models.FloatField()
    humidity = models.FloatField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.created_at.strftime('%Y-%m-%d %H:%M:%S')} | Temp: {self.temperature}°C - Hum: {self.humidity}%"