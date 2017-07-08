# coding=utf-8
from django.shortcuts import render,redirect
from django.http import JsonResponse
from models import *
from hashlib import sha1
from user_decorators import *
import datetime

# Create your views here.
#注册
def register(request):
    context={'title':'注册','top':'0'}
    return render(request,'users/register.html',context)
#注册处理
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
#注册验证
def register_yz(request):
    uname = request.GET.get('uname')
    #去数据库查询uname的行,有就返回1,没有就0
    result = UserInfo.objects.filter(uname=uname).count()
    context = {'result':result}
    return JsonResponse(context)
#登录
def login(request):
    # cookie=request.COOKIE
    # uname = cookie.get('uname')
    #获取cookie中的uname的值,没有值的给它一个默认值''n
    uname = request.COOKIES.get('uname','')
    context = {'title':'登录','uname':uname,'top':'0'}

    return render(request,'users/login.html',context)
#登录验证
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
    context={'title':'登录','uname':uname,'upwd':upwd,'top':'0'}
    # 根据用户名查询数据库,存在返回[对象],不存在返回[]
    user = UserInfo.objects.filter(uname=uname)
    if len(user)==0:
        # 用户名错误或不存在
        context['name_error']='1'
        return render(request,'users/login.html',context)
    else:
        # 判断密码正确
        if user[0].upwd == upwd_sha1:
            #记录当前登录的用户名
            request.session['uid'] = user[0].id
            request.session['uname'] = uname
            #自定义的中间件
            path  = request.session.get('url_path','/')
            response = redirect(path)
            #redirect是HttpResponse的子类,所以继承父类的设置cookie方法
            if user_save=='1':
                #设置cookie的第一个参数是键,第二个参数是值,不给默认是'',第三个参数可以设置过期时间(当前时间往后加天数)
                response.set_cookie('uname',uname,expires=datetime.datetime.now()+datetime.timedelta(days = 7))
            else:
                response.set_cookie('uname','',max_age=-1)
            return response


        else:
            # 密码错误
            context['pwd_error']='1'
            return render(request,'users/login.html',context)
#退出
def loginout(request):
    request.session.flush()
    return redirect('/user/login/')
#个人信息
@user_login
def info(request):
    user = UserInfo.objects.get(pk=request.session['uid'])
    context={'title':'用户中心','user':user}
    return render(request,'users/info.html',context)
#全部订单
@user_login
def order(request):
    context = {'title': '用户中心'}
    return render(request, 'users/order.html', context)
#收货地址
@user_login
def addr(request):

    #例：查询书名为“天龙八部”的所有英雄
    #list = HeroInfo.objects.filter(hbook__btitle='天龙八部')
    # 查询当前登录id的所有的收货信息
    addrmsg = TakeInfo.objects.filter(userid__pk=request.session['uid'])
    context = {'title': '用户中心','addrmsg':addrmsg}
    return render(request, 'users/addr.html', context)
#收货信息处理
def addr_handle(request):
    #接收请求

    print request.session['uid']
    post = request.POST
    tname = post.get('tname')
    taddr = post.get('tname')
    tcode = post.get('tcode')
    tphone = post.get('tphone')
    #创建对象
    takeinfo = TakeInfo()
    takeinfo.tname = tname
    takeinfo.taddr = taddr
    takeinfo.tcode = tcode
    takeinfo.tphone = tphone
    #先获取当前登录用户的实例对象
    user=UserInfo.objects.get(id=request.session['uid'])
    #设置外键对应实例对象
    takeinfo.userid = user
    takeinfo.save()
    return redirect('/user/addr/')