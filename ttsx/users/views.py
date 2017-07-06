# coding=utf-8
from django.shortcuts import render,redirect
from django.http import JsonResponse
from models import *
from hashlib import sha1
import datetime
# Create your views here.

def register(request):
    context={'title':'注册'}
    return render(request,'users/register.html',context)

def register_handle(requset):
    # 接收请求
    post = requset.POST
    uname = post.get('uname')
    upwd = post.get('upwd')
    umail = post.get('email')
    #sha1加密
    s1 = sha1()
    s1.update(upwd)
    upwd_sha1 = s1.hexdigest()
    # 创建对象
    user = UserInfo()
    user.uname=uname
    user.upwd=upwd_sha1
    user.umail=umail
    user.save()
    # 转向
    return redirect('/user/login/')

def register_yz(request):
    uname = request.GET.get('uname')
    #去数据库查询uname的行,有就返回1,没有就0
    result = UserInfo.objects.filter(uname=uname).count()
    context = {'result':result}
    return JsonResponse(context)

def login(request):
    # cookie=request.COOKIE
    # uname = cookie.get('uname')
    #获取cookie中的uname的值
    uname = request.COOKIES.get('uname')
    print 'uname的值为:%s'%uname
    context = {'title':'登录','uname':uname}

    return render(request,'users/login.html',context)

def login_handle(request):
    # 接收请求
    post = request.POST
    uname = post.get('uname')
    upwd = post.get('upwd')
    user_save = post.get('user_save','0')
    # 加密
    s1 = sha1()
    s1.update(upwd)
    upwd_sha1 = s1.hexdigest()
    context={'title':'登录','uname':uname,'upwd':upwd}
    # 根据用户名查询数据库,存在返回[对象],不存在返回[]
    user = UserInfo.objects.filter(uname=uname)
    if len(user)==0:
        # 用户名错误或不存在
        context['name_error']='1'
        return render(request,'users/login.html',context)
    else:
        # 判断密码正确
        if user[0].upwd == upwd_sha1:
            response = redirect('/user/')
            #redirect是HttpResponse的子类,所以继承父类的设置cookie方法
            if user_save=='1':
                #设置cookie的第一个参数是键,第二个参数是值,不给默认是'',第三个参数可以设置过期时间(当前时间往后加天数)
                response.set_cookie('uname',uname,expires=datetime.datetime.now()+datetime.timedelta(days = 7))
            return response


        else:
            # 密码错误
            context['pwd_error']='1'
            return render(request,'users/login.html',context)