# stores/admin.py
from django.contrib import admin
from .models import Store
from django.utils.html import format_html # Để hiển thị ảnh thumbnail (tùy chọn)

class StoreAdmin(admin.ModelAdmin):
    # Thêm 'image' vào list_display để xem đường dẫn ảnh
    # Thêm 'display_image' để xem ảnh thu nhỏ (tùy chọn)
    list_display = ('name', 'address', 'opening_hours', 'display_image', 'latitude', 'longitude')
    readonly_fields = ('image_thumbnail',) # Để hiển thị ảnh trong form sửa (tùy chọn)
    list_filter = ('address',)
    search_fields = ('name', 'address')

    # Đảm bảo 'image' có trong fieldsets nếu bạn dùng fieldsets
    fieldsets = (
        (None, {'fields': ('name', 'address', 'opening_hours', 'phone_number', 'image', 'image_thumbnail')}), # Thêm image và image_thumbnail
        ('Coordinates', {'fields': ('latitude', 'longitude'), 'classes': ('collapse',)}),
    )

    # Hàm tùy chọn để hiển thị ảnh thu nhỏ trong list_display
    def display_image(self, obj):
        if obj.image:
            return format_html('<img src="{}" width="50" height="50" style="object-fit: cover;" />', obj.image.url)
        return "(No Image)"
    display_image.short_description = 'Ảnh' # Đặt tên cột

    # Hàm tùy chọn để hiển thị ảnh thu nhỏ trong form chỉnh sửa
    def image_thumbnail(self, obj):
        if obj.image:
            return format_html('<img src="{}" width="200" style="max-height: 200px;" />', obj.image.url)
        return "(No Image)"
    image_thumbnail.short_description = 'Ảnh hiện tại'

admin.site.register(Store, StoreAdmin)