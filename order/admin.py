from django.contrib import admin
from order.models import Customer, Stock, CusAddr, Order

# Register your models here.
class CustomerAdmin(admin.ModelAdmin):
    list_display = ('cus_mail', 'cus_name', 'cus_addr', 'cus_phone')

admin.site.register(Customer, CustomerAdmin)

class StockAdmin(admin.ModelAdmin):
    list_display = ('id', 'st_name', 'st_quantity', 'st_price')

admin.site.register(Stock, StockAdmin)

class CusAddrAdmin(admin.ModelAdmin):
    list_display = ('ca_mail', 'ca_name', 'ca_addr', 'ca_phone')

admin.site.register(CusAddr, CusAddrAdmin)

class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'ord_cid', 'ord_pid', 'ord_cname', 'ord_addr', 'ord_phone', 'ord_quantity', 'state', 'ord_date')

admin.site.register(Order, OrderAdmin)