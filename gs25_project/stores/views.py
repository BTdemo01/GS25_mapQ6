# stores/views.py

from django.shortcuts import render
# Sử dụng geopy để geocode với Nominatim và tính khoảng cách
from geopy.geocoders import Nominatim
from geopy.distance import distance as geopy_distance
from geopy.exc import GeocoderTimedOut, GeocoderServiceError # Để bắt lỗi từ geopy
# Import model Store (giả sử bạn đã tạo nó trong models.py)
from .models import Store
import json # Để chuyển đổi dữ liệu Python thành JSON cho Javascript

# --- View cho Trang chủ (có chức năng lọc) ---
def home_view(request):
    """
    Hiển thị trang chủ, bản đồ và danh sách cửa hàng.
    Xử lý lọc cửa hàng dựa trên vị trí và khoảng cách người dùng nhập (sử dụng Nominatim).
    """
    # Lấy tất cả cửa hàng có tọa độ hợp lệ từ database
    # Nên tối ưu query này nếu có nhiều cửa hàng
    stores_qs = Store.objects.filter(latitude__isnull=False, longitude__isnull=False)

    # Khởi tạo các biến
    user_lat = None
    user_lon = None
    search_location = request.GET.get('location', "") # Lấy vị trí tìm kiếm từ URL
    distance_query = request.GET.get('distance', "") # Lấy khoảng cách từ URL
    error_message = None # Thông báo lỗi cho người dùng
    filtered_stores = list(stores_qs) # Mặc định hiển thị tất cả cửa hàng hợp lệ

    # Chỉ thực hiện Geocoding và lọc nếu người dùng nhập vị trí
    if search_location:
        try:
            # Khởi tạo Nominatim - BẮT BUỘC đặt user_agent duy nhất!
            # Thay 'your_unique_app_name/1.0' bằng tên định danh ứng dụng của bạn
            geolocator = Nominatim(user_agent="gs25_store_locator_django_app/1.0")

            print(f"Đang geocode địa chỉ: {search_location}") # Dùng để debug
            # Gọi API Nominatim để lấy tọa độ
            location = geolocator.geocode(search_location, timeout=10, country_codes='vn')

            if location:
                user_lat = location.latitude
                user_lon = location.longitude
                print(f"Tìm thấy tọa độ: Lat={user_lat}, Lon={user_lon}") # Dùng để debug

                # Thực hiện tính toán khoảng cách và lọc
                stores_with_distance = []
                user_coords = (user_lat, user_lon)

                for store in stores_qs:
                    # Đảm bảo store có tọa độ hợp lệ trước khi tính
                    if store.latitude is not None and store.longitude is not None:
                        store_coords = (store.latitude, store.longitude)
                        try:
                            dist_km = geopy_distance(user_coords, store_coords).km
                            # Kiểm tra khoảng cách lọc
                            limit_km = None
                            if distance_query:
                                try:
                                    limit_km = float(distance_query)
                                except ValueError:
                                    pass # Bỏ qua nếu giá trị khoảng cách không hợp lệ

                            if limit_km is None or dist_km <= limit_km:
                                stores_with_distance.append({'store': store, 'distance': round(dist_km, 2)})

                        except ValueError:
                             # Lỗi nếu tọa độ không hợp lệ
                             print(f"Bỏ qua store ID {store.id} do tọa độ không hợp lệ.")
                    else:
                        print(f"Bỏ qua store ID {store.id} do thiếu tọa độ.")


                # Sắp xếp các cửa hàng theo khoảng cách gần nhất
                stores_with_distance.sort(key=lambda item: item['distance'])
                # Lấy danh sách các đối tượng Store đã lọc và sắp xếp
                filtered_stores = [item['store'] for item in stores_with_distance]

            else:
                # Xử lý khi Nominatim không tìm thấy địa chỉ
                error_message = f"Không thể tìm thấy tọa độ cho vị trí: '{search_location}'. Vui lòng thử nhập địa chỉ rõ ràng hơn."
                print(error_message)
                filtered_stores = [] # Không hiển thị cửa hàng nào nếu không tìm thấy vị trí

        except GeocoderTimedOut:
            error_message = "Yêu cầu tìm kiếm vị trí bị quá thời gian chờ. Vui lòng thử lại."
            print(error_message)
            filtered_stores = []
        except GeocoderServiceError as e:
            error_message = f"Lỗi dịch vụ tìm kiếm vị trí từ OpenStreetMap: {e}. Vui lòng thử lại sau."
            print(error_message)
            filtered_stores = []
        except Exception as e: # Bắt các lỗi không mong muốn khác
             error_message = f"Đã xảy ra lỗi trong quá trình xử lý: {e}"
             print(error_message)
             filtered_stores = []

    # Chuẩn bị dữ liệu cho JavaScript (Leaflet map)
    # Chỉ bao gồm các cửa hàng đã được lọc (hoặc tất cả nếu không tìm kiếm)
    stores_data_for_js = []
    for store in filtered_stores:
         # Chỉ thêm vào JS nếu store có tọa độ
         if store.latitude is not None and store.longitude is not None:
             stores_data_for_js.append({
                 'id': store.id,
                 'name': store.name,
                 'address': store.address,
                 'lat': store.latitude,
                 'lng': store.longitude,
                 'phone': store.phone_number or '', # Thêm sđt nếu cần hiển thị trên marker popup
             })

    # Dữ liệu truyền ra template
    context = {
        'stores': filtered_stores, # Danh sách store objects cho vòng lặp HTML
        'stores_data_for_js': json.dumps(stores_data_for_js), # Dữ liệu JSON cho Javascript
        'user_lat': user_lat, # Tọa độ người dùng (nếu tìm thấy)
        'user_lon': user_lon, # Tọa độ người dùng (nếu tìm thấy)
        'search_location': search_location, # Giữ lại giá trị người dùng đã nhập
        'search_distance': distance_query, # Giữ lại khoảng cách người dùng đã chọn
        'error_message': error_message, # Truyền thông báo lỗi (nếu có)
    }
    return render(request, 'stores/home.html', context)


# --- View cho Trang Giới thiệu ---
def gioi_thieu_view(request):
    """Hiển thị trang giới thiệu."""
    context = {}
    return render(request, 'stores/gioi_thieu.html', context)


# --- View cho Trang Sản phẩm ---
def san_pham_view(request):
    """
    Hiển thị trang sản phẩm.
    TODO: Hiện tại đang dùng template tĩnh. Cần cập nhật để lấy sản phẩm từ database.
    """
    # Ví dụ sau này:
    # from .models import Product
    # products = Product.objects.all()
    context = {
        # 'products': products
    }
    return render(request, 'stores/san_pham.html', context)


# --- View cho Trang Liên hệ ---
def lien_he_view(request):
    """Hiển thị trang liên hệ."""
    context = {}
    return render(request, 'stores/lien_he.html', context)


# --- (Tùy chọn) View cho Trang chi tiết cửa hàng ---
# def store_detail_view(request, store_id):
#     """Hiển thị thông tin chi tiết của một cửa hàng."""
#     try:
#         store = Store.objects.get(pk=store_id)
#         context = {'store': store}
#         return render(request, 'stores/store_detail.html', context)
#     except Store.DoesNotExist:
#         # Xử lý trường hợp không tìm thấy store
#         # Ví dụ: trả về trang 404
#         from django.http import Http404
#         raise Http404("Cửa hàng không tồn tại")