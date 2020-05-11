from django.conf.urls import url
from django.contrib import admin
from django.urls import path
from myapp import views

urlpatterns = [
    url('ProductShow/', views.pproducts, name='pp'),
    #path('<int:pk>/',views.cart,name='cart'),
    url(r'^(?P<pk>[0-9]+)/$', views.display, name='display'),
]