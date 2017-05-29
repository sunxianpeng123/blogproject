# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render

from django.http import HttpResponse
from django.shortcuts import render,get_object_or_404
from .models import Post,Category,Tag
import markdown
from comments.forms import CommentForm
# Create your views here.
"""
这里我们不再是直接把字符串传给 HttpResponse 了，而是调用 Django 提供的 render 函数。这个函数根据我们传入的参数来构造 HttpResponse。

我们首先把 HTTP 请求传了进去，然后 render 根据第二个参数的值 blog/index.html 找到这个模板文件并读取模板中的内容。
之后 render 根据我们传入的 context 参数的值把模板中的变量替换为我们传递的变量的值，
{{ title }} 被替换成了 context 字典中 title 对应的值，同理 {{ welcome }} 也被替换成相应的值。
"""

def index(request):
    postList=Post.objects.all().order_by('-createTime')
    #return render(request,'blog/index.html',context={'title':"我的博客首页",'welcome':"欢迎访问我的博客首页"})
    #排序依据的字段是 created_time，即文章的创建时间。- 号表示逆序，如果不加 - 则是正序。

    return render(request,'blog/index.html',context={'postList':postList})

def detail(request,pk):
    """视图函数很简单，它根据我们从 URL 捕获的文章 id（
    也就是 pk，这里 pk 和 id 是等价的）获取数据库中文章
    id 为该值的记录，然后传递给模板。注意这里我们用到了从
     django.shortcuts 模块导入的 get_object_or_404 方法，其
     作用就是当传入的 pk 对应的 Post 在数据库存在时，就返回对
     应的 post，如果不存在，
    就给用户返回一个 404 错误，表明用户请求的文章不存在。"""
    post=get_object_or_404(Post,pk=pk)
    post.body=markdown.markdown(post.body,extecsions=[
                                    'markdown.extensions.extra',
                                     'markdown.extensions.codehilite',
                                     'markdown.extensions.toc',])
    # 记得在顶部导入 CommentForm
    form = CommentForm()
    # 获取这篇 post 下的全部评论
    commentList = post.comment_set.all()
    # 将文章、表单、以及文章下的评论列表作为模板变量传给 detail.html 模板，以便渲染相应数据。
    context = {'post': post,
               'form': form,
               'commentList': commentList
               }
    return render(request, 'blog/detail.html', context=context)

def archives(request, year, month):
    """归档视图"""
    post_list = Post.objects.filter(created_time__year=year,
                                    created_time__month=month
                                    ).order_by('-created_time')
    return render(request, 'blog/index.html', context={'post_list': post_list})

def category(request,pk):
    """分类页面的视图函数
    这里我们首先根据传入的 pk 值（也就是被访问的分类的 id 值）从数据库中获取到这个分类。get_object_or_404 函数和 detail 视图中一样，其作用是如果用户访问的分类不存在，则返回一个 404 错误页面以提示用户访问的资源不存在。然后我们通过 filter 函数过滤出了该分类下的全部文章。同样也和首页视图中一样对返回的文章列表进行了排序。
    """
    cate=get_object_or_404(Category,pk=pk)
    postList=Post.objects.filter(category=cate).order_by('-createTime')
    return render(request,'blog/index.html',context={'postList':postList})

def search(request):
    """首先我们使用 request.GET.get('q') 获取到用户提交的搜索关键词。用户通过表单提交的数据 django 为我们保存在 request.GET 里，这是一个类似于 Python 字典的对象，所以我们使用 get 方法从字典里取出键 q 对应的值，即用户的搜索关键词。这里字典的键之所以叫 q 是因为我们的表单中搜索框 input 的 name 属性的值是 q，如果修改了 name 属性的值，那么这个键的名称也要相应修改。"""
    q=request.GET.get('q')
    errorMsg=''
    if not q:
        errorMsg='请输入关键词'
        return render(request,'blog/errors.html',{'errorMsg':errorMsg})
    postList=Post.objects.filter(title__contains=q)#过滤条件是 title__icontains=q，即 title 中包含（contains）关键字 q，前缀 i 表示不区分大小写。这里 icontains 是查询表达式（Field lookups），其用法是在模型需要筛选的属性后面跟上两个下划线。
    return render(request,'blog/results.html',{'errorMsg':errorMsg,'postList':postList})
