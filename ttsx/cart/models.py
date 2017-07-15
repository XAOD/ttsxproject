from django.db import models
# Create your models here.


class CartInfo(models.Model):
    user = models.ForeignKey('users.UserInfo')
    goods = models.ForeignKey('goods.GoodsInfo')
    count = models.IntegerField()