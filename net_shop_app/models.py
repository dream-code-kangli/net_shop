from django.db import models


# Create your models here.


class Category(models.Model):
    cname = models.CharField(max_length=20, verbose_name='商品分类')

    def __str__(self):
        return self.cname


class Goods(models.Model):
    gname = models.CharField(max_length=100, verbose_name='商品名称')
    gdesc = models.CharField(max_length=100, verbose_name='商品描述')
    oldprice = models.DecimalField(max_digits=5, decimal_places=2, verbose_name='原价')
    price = models.DecimalField(max_digits=5, decimal_places=2, verbose_name='现价')
    category = models.ForeignKey(Category, on_delete=models.CASCADE, verbose_name='类别ID')

    def getImgUrl(self):
        # print(self.inventory_set.first().color.color)
        return self.inventory_set.first().color.color

    def getColor(self):
        colors = []
        for inventory in self.inventory_set.all():
            color = inventory.color
            if color not in colors:
                colors.append(color)
        return colors

    def getSize(self):
        sizes = []
        for inventory in self.inventory_set.all():
            size = inventory.size
            if size not in sizes:
                sizes.append(size)
        return sizes

    def getDetailInfo(self):
        datas = {}
        for detail in self.goodsdetail_set.all():
            detailName = detail.getDname()
            if detailName not in datas:
                datas[detailName] = [detail.gdurl]
            else:
                datas[detailName].append(detail.gdurl)
        return datas

    def __str__(self):
        return self.gname


class GoodsDetailName(models.Model):
    gdname = models.CharField(max_length=30, verbose_name='详情名称')

    def __str__(self):
        return self.gdname


class GoodsDetail(models.Model):
    gdurl = models.ImageField(upload_to='', verbose_name='详情图片地址')
    detail = models.ForeignKey(GoodsDetailName, on_delete=models.CASCADE)
    goods = models.ForeignKey(Goods, on_delete=models.CASCADE)

    def getDname(self):
        return self.detail.gdname

    def __str__(self):
        return self.detail.gdname


class Size(models.Model):
    sname = models.CharField(max_length=10, verbose_name='尺寸名称')

    def __str__(self):
        return self.sname


class Color(models.Model):
    colorname = models.CharField(max_length=10, verbose_name='颜色名称')
    color = models.ImageField(upload_to='color/', verbose_name='颜色图片地址')

    def __str__(self):
        return self.colorname


class Inventory(models.Model):
    count = models.PositiveIntegerField(verbose_name='库存数量')
    color = models.ForeignKey(Color, on_delete=models.CASCADE)
    goods = models.ForeignKey(Goods, on_delete=models.CASCADE, related_name='inventory_set')
    size = models.ForeignKey(Size, on_delete=models.CASCADE)

    def __str__(self):
        return self.count

