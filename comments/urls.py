# coding: utf-8
"""
@author: sunxianpeng
@file: urls.py
@time: 2017/5/27 22:01
"""
from django.conf.urls import url
from . import views
#别忘了给这个评论的 URL 模式规定命名空间，即 app_name = 'comments'。
amm_name='comments'

urlpatterns=[
    url(r'^comment/post/(?P<post_pk>[0-9]+)/$', views.post_comment, name='post_comment'),

]