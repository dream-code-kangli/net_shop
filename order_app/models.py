from django.db import models
from user_app.models import Address, UserInfo


# Create your models here.
class TradeOrder(models.Model):
    out_order_num = models.UUIDField()
    order_num = models.CharField(max_length=50)
    status = models.CharField(max_length=20, default='待支付')
    payway = models.CharField(max_length=20, default='alipay')
    address = models.ForeignKey(Address, on_delete=models.CASCADE)
    user = models.ForeignKey(UserInfo, on_delete=models.CASCADE)

    def __str__(self):
        return self.order_num


class TradeOrderItem(models.Model):
    goodsid = models.PositiveIntegerField()
    colorid = models.PositiveIntegerField()
    sizeid = models.PositiveIntegerField()
    count = models.PositiveIntegerField()
    order = models.ForeignKey(TradeOrder, on_delete=models.CASCADE)
