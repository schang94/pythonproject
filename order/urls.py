from django.urls import path
from order import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.OrderList, name='order_list'),
    path('search/', views.OrderListSearch, name='order_list_search'),
    path('odetail/', views.OrderDetail, name='order_detail'),
    path('ostch/', views.OrderChage, name='order_change'),
    path('stock/', views.StockList, name='stock_list'),
    path('stock/detail/', views.StockDetail, name='stock_detail'),
    path('stock/delete/', views.StockDelete, name='stock_delete'),
    path('stock/modify/', views.StockModify, name='stock_modify_page'),
    path('stock/modifyOk/', views.StockModifyOk, name='stock_modify_ok'),
    path('stock/insert/', views.StockInsert, name='stock_insert_page'),
    path('stock/insertOk/', views.StockInsertOk, name='stock_insert_ok'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root = settings.STATIC_ROOT)

