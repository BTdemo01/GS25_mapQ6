from django.db import models

class Store(models.Model):
    # Các trường của bạn ở đây, ví dụ:
    name = models.CharField(max_length=200)
    address = models.TextField()
    phone_number = models.CharField(max_length=20, blank=True, null=True)
    latitude = models.FloatField(null=True, blank=True)
    longitude = models.FloatField(null=True, blank=True)

    def __str__(self):
        return self.name