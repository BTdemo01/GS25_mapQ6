from django.db import models

class Store(models.Model):
    # Các trường của bạn ở đây, ví dụ:
    name = models.CharField(max_length=200)
    opening_hours = models.CharField(
        "Giờ mở cửa",  # Nhãn hiển thị (ví dụ trong admin)
        max_length=150,
        blank=True,     # Cho phép để trống trong form
        null=True       # Cho phép giá trị NULL trong database
    )
    address = models.TextField()
    phone_number = models.CharField(max_length=20, blank=True, null=True)
    latitude = models.FloatField(null=True, blank=True)
    longitude = models.FloatField(null=True, blank=True)
    image = models.ImageField(
        "Hình ảnh",                  # Nhãn hiển thị
        upload_to='store_images/',   # Thư mục con trong MEDIA_ROOT để lưu ảnh store
        blank=True,                  # Cho phép để trống trong form admin
        null=True                    # Cho phép giá trị NULL trong database (không bắt buộc có ảnh)
    )

    def __str__(self):
        return self.name