from django.db import models

# Create your models here.
class Customer(models.Model):
    cus_mail = models.CharField(max_length = 20, primary_key=True)
    cus_passwd = models.CharField(max_length = 30)
    cus_name = models.CharField(max_length = 20)
    cus_addr = models.CharField(max_length = 50)
    cus_phone = models.CharField(max_length = 20)
    cus_authority = models.BooleanField()
    
class Stock(models.Model):
    st_name = models.CharField(max_length = 50)
    st_quantity = models.IntegerField()
    st_price = models.IntegerField()
    
    def __str__(self):
        return self.st_name

class CusAddr(models.Model):
    ca_mail = models.ForeignKey(Customer, on_delete=models.CASCADE)
    ca_name = models.CharField(max_length = 20)
    ca_addr = models.CharField(max_length = 50)
    ca_phone = models.CharField(max_length = 20)
    
class Order(models.Model):
    ord_cid = models.ForeignKey(Customer, on_delete=models.CASCADE)
    ord_pid = models.ForeignKey(Stock, on_delete=models.CASCADE)
    ord_cname = models.CharField(max_length = 20)
    ord_addr = models.CharField(max_length = 50)
    ord_phone = models.CharField(max_length = 20)
    ord_quantity = models.IntegerField()
    state = models.IntegerField()
    ord_date = models.DateTimeField()
    


    
    
