from .views import *
from django.urls import path
from .views import get_paste, create_paste_page, paste_detail_page
from django.urls import path
from myapp.views import paste_list

urlpatterns = [
    path("paste/", create_paste, name="create_paste"),
    path("paste/<uuid:paste_id>/", get_paste, name="get_paste"),
    path("paste/<uuid:paste_id>/delete/", delete_paste, name="delete_paste"),
    path("", create_paste_page, name="home"),
    path("view/<uuid:paste_id>/", paste_detail_page, name="paste_detail"),
]

urlpatterns += [
    path('', create_paste_page, name='home'),
    path('<uuid:paste_id>/', paste_detail_page, name='paste_detail'),  # 👈 Thêm URL này
]


urlpatterns += [
    path("pastes/", paste_list, name="paste_list"),
]

urlpatterns += [
    path('paste/<int:paste_id>/delete/', delete_paste, name='paste_delete'),
]

urlpatterns += [
    path("pastes/delete_expired/", delete_expired_pastes, name="delete_expired_pastes"),
]