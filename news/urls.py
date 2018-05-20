
# -*- coding:utf-8 -*-
#  made in ly

from django.conf.urls import url
from . import views

app_name='news'
urlpatterns = [
    url(r'^$', views.IndexView.as_view(), name = 'index'),
  #  url(r'^category/(?P<pk>[0-9]+)/$', views.CategoryView.as_view(), name="category"),
    url(r'^category/(?P<pk>[0-9]+)/$', views.category, name="category"),
]
