# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from .models import Post,Category,Tag

# Register your models here.
"""
要在后台注册我们自己创建的几个模型，这样 Django Admin 才能知道它们的存在，注册非常简单，只需要在 blog\admin.py 中加入下面的代码：
你可能想往文章内容中添加图片，但目前来说还做不到。在支持 Markdown 语法部分中将介绍如何在文章中插入图片的方法。
"""
admin.site.register(Post)
admin.site.register(Category)
admin.site.register(Tag)
