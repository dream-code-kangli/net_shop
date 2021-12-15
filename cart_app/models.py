from django.db import models


# Create your models here.
from user_app.models import UserInfo
from net_shop_app.models import Color, Size, Goods


class CartItem(models.Model):
    goodsid = models.PositiveIntegerField()
    colorid = models.PositiveIntegerField()
    sizeid = models.PositiveIntegerField()
    count = models.PositiveIntegerField(default=0)
    isdelete = models.BooleanField(default=False)
    user = models.ForeignKey(UserInfo, on_delete=models.CASCADE)

    def getColor(self):
        return Color.objects.get(id=self.colorid)

    def getSize(self):
        return Size.objects.get(id=self.sizeid)

    def getGood(self):
        return Goods.objects.get(id=self.goodsid)

    def getTotalPrice(self):
        return int(self.getGood().price)*int(self.count)



