from django.conf.urls import url
import views
urlpatterns = [
    url(r'^add/$',views.add),
    url(r'^count/$',views.count),
    url(r'^$',views.cart),
]