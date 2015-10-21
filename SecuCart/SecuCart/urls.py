from django.conf.urls import patterns, url, include
from django.contrib import admin
from SecuCart import views

urlpatterns = patterns('',
    url(r'^admin/', include(admin.site.urls)),
    url(r'^$', views.home, name='home'),
    url(r'^inventory/$', views.inventory, name='inventory'),
    url(r'^login/$', views.login, name='login'),
    url(r'^shopping_cart/$', views.shopping_cart, name='shopping_cart')
)
