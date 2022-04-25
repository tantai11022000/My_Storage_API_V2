from django.db import models
from pkg_resources import require
from storage.models import Goods
class Bill(models.Model):
    
    name = models.CharField(max_length=200)
    address = models.CharField(max_length=250)
    phone = models.CharField(max_length=13)
    code = models.CharField(max_length=200,unique=True)

    def __str__(self):
        return self.code


class BillDetail(models.Model):
    billCode = models.ForeignKey(Bill,on_delete=models.SET_NULL,null=True,related_name="bill_detail")
    codeGood = models.ForeignKey(Goods,on_delete=models.SET_NULL,null=True,related_name="good_detail")
    amount = models.IntegerField(null=False)
    price = models.FloatField(null=False)