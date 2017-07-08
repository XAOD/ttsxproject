from django.conf.urls import url
import views

urlpatterns=[
    url(r'^register/$',views.register),
    url(r'^register_handle/$',views.register_handle),
    url(r'^register_yz/$',views.register_yz),
    url(r'^login/$',views.login),
    url(r'^login_handle/$',views.login_handle),
    url(r'^loginout/$',views.loginout),
    url(r'^$',views.info),
    url(r'^order/$',views.order),
    url(r'^addr/$',views.addr),
    url(r'^addr_handle/$',views.addr_handle),

]