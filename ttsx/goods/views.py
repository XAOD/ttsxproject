#coding=utf-8
from django.shortcuts import render
from models import *
from django.core.paginator import Paginator
from haystack.generic_views import SearchView
# Create your views here.

#首页
def index(request):
    goodslist = []#---{'type':type,'newlist':newlist,'clicklist':clicklist}
    # 查询分类对象
    # 查询每个分类中最新的4个商品
    # 查询每个分类中最火的4个商品
    typelist = TypeInfo.objects.all()
    for type in typelist:
        newlist = type.goodsinfo_set.order_by('-id')[0:4]
        clicklist = type.goodsinfo_set.order_by('-gclick')[0:4]
        goodslist.append({'type':type,'newlist':newlist,'clicklist':clicklist})
    context = {'title':'首页','glist':goodslist,'shopcar_show':'1'}
    return render(request,'goods/index.html',context)
#列表页
def list(request,tid,pindex,orderby):#参数分别对应:request,分类,页码,排序规则
    try:
        type = TypeInfo.objects.get(pk=int(tid))
        # 查询当前分类中最新的两个商品
        newlist = type.goodsinfo_set.order_by('-id')[0:2]
        #定义排序规则
        desc = '1'
        orderby_str = '-id'#默认id降序'
        if orderby == '2':#价格排序
            desc = request.GET.get('desc','1')
            if desc == '1':#降序
                orderby_str = '-gprice'
                # desc = '0'
            else:#升序
                orderby_str = 'gprice'
                # desc = '1'
        elif orderby == '3':
            #按人气排序
            orderby_str = '-gclick'
        # 查询当前分类的所有商品
        glist = type.goodsinfo_set.order_by(orderby_str)
        # 按每页几个来显示
        paginator = Paginator(glist,1)
        pindex1 = int(pindex)
        #控制用户输入的页码在范围内
        if pindex1<1:
            pindex1 = 1
        elif pindex1 > paginator.num_pages:
            pindex1 = paginator.num_pages
        page = paginator.page(pindex1)
        context = {'title':'商品列表页','shopcar_show':'1','type':type,'newlist':newlist,'page':page,'orderby':orderby,'desc':desc}
        return render(request,'goods/list.html',context)
    except:
        return render(request,'404.html')
#商品详情页
def detail(request,id):
    try:
        goods = GoodsInfo.objects.get(pk=id)
        #浏览一次,点击量加1
        goods.gclick+=1
        goods.save()
        #根据商品的所属类型查询最新的两个商品
        newlist = goods.gtype.goodsinfo_set.order_by('-id')[0:2]
        context = {'title':'商品详情页','shopcar_show':'1','goods':goods,'newlist':newlist}
        response = render(request,'goods/detail.html',context)
        #保存最近浏览,split(把字符串切割成列表),join(把字符串列表组成字符串)
        #先读取已经存的,进行拼接
        gids = request.COOKIES.get('goodsid','').split(',')
        #判断是否存在,若存在,则删除
        if id in gids:
            gids.remove(id)
        gids.insert(0,id)#加到最前面
        #如果超过5个,则删除最后一个
        if len(gids)>6:
            gids.pop()
        response.set_cookie('goodsid',','.join(gids),max_age=60*60*24*7)

        return response
    except:
        return render(request,'404.html')
#自定义全文检索视图
class MySearchView(SearchView):
    def get_context_data(self, *args, **kwargs):
        context = super(MySearchView, self).get_context_data(*args, **kwargs)
        context['shopcar_show']='1'
        page_range = []
        page = context.get('page_obj')
        if page.paginator.num_pages<5:#总页数小于5
            page_range = page.paginator.page_range#[1,2,3,4]
        elif page.number<=2:#当前页是第一页或第二页
            page_range = range(1,6)#[1,2,3,4,5]
        elif page.number>=page.paginator.num_pages-1:#当前页是倒数第一页或倒数第二页
            page_range = range(page.paginator.num_pages-4,page.paginator.num_pages+1)#[6,7,8,9,10]
        else:
            page_range = range(page.number-2,page.number+3)
        context['page_range']=page_range
        return context
'''
    列表页排序,排序,页码控制
    最近浏览
    全文检索

'''