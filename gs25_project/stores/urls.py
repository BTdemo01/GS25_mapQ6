from django.urls import path
from . import views # Import views từ app hiện tại

app_name = 'stores' # Đặt tên cho namespace (tùy chọn nhưng nên có)

urlpatterns = [
    path('', views.home_view, name='home'), # URL gốc '' sẽ gọi home_view
    path('gioithieu/', views.gioi_thieu_view, name='gioi_thieu'),
    path('sanpham/', views.san_pham_view, name='san_pham'),
    path('lienhe/', views.lien_he_view, name='lien_he'),
    path('<int:store_id>/', views.store_detail_view, name='store_detail'),
]   