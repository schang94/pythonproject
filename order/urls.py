from django.urls import path
from order import views

urlpatterns = [
    path('', views.OrderList, name='order_list'),
    path('search/', views.OrderListSearch, name='order_list_search'),
    path('odetail/', views.OrderDetail, name='order_detail'),
    path('ostch/', views.OrderChage, name='order_change'),
    path('stock/', views.StockList, name='stock_list'),
    path('stock/detail/', views.StockDetail, name='stock_detail'),
    path('stock/modify/', views.StockModify, name='stock_modify_page'),
    path('stock/modifyOk/', views.StockModifyOk, name='stock_modify_ok'),
    path('stock/insert/', views.StockInsert, name='stock_insert_page'),
    path('stock/insertOk/', views.StockInsertOk, name='stock_insert_ok'),
]
