#coding=utf-8
from django.shortcuts import redirect
def user_login(func):
    def func1(request,*args,**kwargs):
        #判断用户是否登录
        if request.session.has_key('uid'):
            #已经登录
            return func(request,*args,**kwargs)
        else:
            return redirect('/user/login/')
    return func1