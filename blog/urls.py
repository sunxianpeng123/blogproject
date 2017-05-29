# coding: utf-8
"""
@author: sunxianpeng
@file: urls.py
@time: 2017/5/24 0:05

注意：在项目根目录的 blogproject\ 目录下
（即 settings.py 所在的目录），原本就有一
个 urls.py 文件，这是整个工程项目的 URL 配置文件。
而我们这里新建了一个 urls.py 文件，且位于 blog 应用下。
这个文件将用于 blog 应用相关的 URL 配置。不要把两个
文件搞混了。
还差最后一步了，我们前面建立了一个 urls.py 文件，
并且绑定了 URL 和视图函数 index，但是 Django 并不知道。
Django 匹配 URL 模式是在 blogproject\ 目录（
即 settings.py 文件所在的目录）的 urls.py 下的，
所以我们要把 blog 应用下的 urls.py 文件包含到
blogproject\urls.py 里去，打开这个文件看到如下内容：

====
比如我们可以把文章详情页面对应的视图设计成这个样子：当用户访问
 <网站域名>/post/1/ 时，显示的是第一篇文章的内容，而当用户访问
 <网站域名>/post/2/ 时，显示的是第二篇文章的内容，这里数字代表了
 第几篇文章，也就是数据库中
 Post 记录的 id 值。下面依照这个规则来绑定 URL 和视图：

"""

from django.conf.urls import url
from . import views

urlpatterns=[
       url(r'^$',views.index,name='index'),
       url(r'^post/(?P<pk>[0-9]+)/$', views.detail, name='detail'),
       url(r'^archives/(?P<year>[0-9]{4})/(?P<month>[0-9]{1,2})/$', views.archives, name='archives'),
       url(r'^category/(?P<pk>[0-9]+)/$', views.category, name='category'),
       url(r'^search/$', views.search, name='search'),
]