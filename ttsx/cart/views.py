#coding=utf-8
from django.shortcuts import render
from django.http import JsonResponse
from models import *
from users.user_decorators import user_login
# Create your views here.
#添加到购物车
def add(request):
    try:
        # 用户,商品,数量
        uid = request.session.get('uid')
        gid = int(request.GET.get('gid'))
        count = int(request.GET.get('count', '1'))
        # 创建cart对象,存进数据库
        # 查询当前用户的同一件商品购物车对象
        # 需求:同一用户添加了同一商品,不再重新网数据库里添加,而是增加count的值
        carts = CartInfo.objects.filter(user_id=uid,goods_id=gid)
        if len(carts)==1:
            carts[0].count+=count
            carts[0].save()
        else:
            cart = CartInfo()
            cart.user_id = uid
            cart.goods_id = gid
            cart.count = count
            cart.save()
        return JsonResponse({'result':1})
    except:
        return JsonResponse({'result':0})
#购物车的几种商品
def count(request):
    uid = request.session.get('uid')
    count = CartInfo.objects.filter(user_id=uid).count()#根据用户id查询对应的商品的行数,也就是几种商品
    return JsonResponse({'count':count})
@user_login
def cart(request):
    #根据当前登陆的用户名查询购物车对象
    uid = request.session.get('uid')
    cartlist = CartInfo.objects.filter(user_id=uid)
    context = {'title':'购物车','cartlist':cartlist}
    return render(request,'carts/cart.html',context)