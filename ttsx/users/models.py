# coding=utf-8
from django.db import models


# Create your models here.
#用户模型类
class UserInfo(models.Model):
    uname = models.CharField(max_length=20)#用户名
    upwd = models.CharField(max_length=40)#密码
    umail = models.CharField(max_length=20)#邮箱
    utel = models.CharField(default='',max_length=20)#联系方式
    uaddr = models.CharField(default='',max_length=100)#地址


#收货信息类
class  TakeInfo(models.Model):
    tname = models.CharField(max_length=10)#收货人
    taddr = models.CharField(max_length=100)#收货地址
    tcode = models.CharField(max_length=6)#邮编
    tphone = models.CharField(max_length=20)#手机号
    userid = models.ForeignKey('UserInfo')#外键