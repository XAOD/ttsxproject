#coding=utf-8
from django.db import models
from tinymce.models import HTMLField
# Create your models here.
# 总商品分类模型类
class TypeInfo(models.Model):
    ttitle = models.CharField(max_length=20)
    isDelete = models.BooleanField(default=False)

    def __str__(self):
        return self.ttitle.encode('utf-8')
# 商品详细类
class GoodsInfo(models.Model):
    gtitle = models.CharField(max_length=50)#商品名
    gimg = models.ImageField(upload_to='goods')#图片
    gprice = models.DecimalField(max_digits=5,decimal_places=2)#价格(999.99)
    gclick = models.IntegerField(default=0)#点击量/人气
    gunit = models.CharField(max_length=20)#单位
    isDelete = models.BooleanField(default=False)
    gsubtitle = models.CharField(max_length=200)#商品简介
    gkucun = models.IntegerField(default=100)#库存
    gcontent = HTMLField()#商品详情(富文本)
    gtype = models.ForeignKey('TypeInfo')
