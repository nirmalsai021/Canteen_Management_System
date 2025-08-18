from django.db import models

class CanteenTiming(models.Model):
    opening_time = models.TimeField(default='09:00')
    closing_time = models.TimeField(default='17:00')

    def __str__(self):
        return f"{self.opening_time} - {self.closing_time}"