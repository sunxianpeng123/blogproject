# coding: utf-8
"""
@author: sunxianpeng
@file: blog_tags.py.py
@time: 2017/5/26 23:17
我们的博客侧边栏有四项内容：最新文章、归档、分类和标签云。这些内容相对比较固定，且在各个页面都会显示，如果像文章列表或者文章详情一样，从视图函数中获取然后传递给模板，则每个页面对应的视图函数里都要写一段获取这些内容的代码，这会导致很多重复代码。更好的解决方案是直接在模板中获取，为此，我们使用 Django 的一个新技术：自定义模板标签来完成任务。
使用模板标签的解决思路

我们前面已经接触过一些 Django 内置的模板标签，比如比较简单的 {% static %} 模板标签，这个标签帮助我们在模板中引入静态文件。还有比较复杂的如 {% for %} {% endfor%} 标签。这里 我们希望自己定义一个模板标签，例如名为 get_recent_posts 的模板标签，它可以这样工作：我们只要在模板中写入 {% get_recent_posts as recent_post_list %}，那么模板中就会有一个从数据库获取的最新文章列表，并通过 as 语句保存到 recent_post_list 模板变量里。这样我们就可以通过 {% for %} {% endfor%} 模板标签来循环这个变量，显示最新文章列表了，这和我们在编写博客首页面视图函数是类似的。首页视图函数中从数据库获取文章列表并保存到 post_list 变量，然后把这个 post_list 变量传给模板，模板使用 for 模板标签循环这个文章列表变量，从而展示一篇篇文章。这里唯一的不同是我们从数据库获取文章列表的操作不是在视图函数中进行，而是在模板中通过自定义的 {% get_recent_posts %} 模板标签进行。

以上就是解决思路，但模板标签不是我们随意写的，必须遵循 Django 的规范我们才能在 Django 的模板系统中使用自定义的模板标签，下面我们就依照这些规范来实现我们的需求。
"""
from ..models import Post,Category
from django import template
from django.db.models.aggregates import Count
register=template.Library()
# Count 计算分类下的文章数，其接受的参数为需要计数的模型的名称

#最新文章模板标签
@register.simple_tag
def getRecentPosts(num=5):
    """
    这个函数的功能是获取数据库中前 num 篇文章，这里 num 默认为 5。函数就这么简单，但目前它还只是一个纯 Python 函数，Django 在模板中还不知道该如何使用它。为了能够通过 {% get_recent_posts %} 的语法在模板中调用这个函数，必须按照 Django 的规定注册这个函数为模板标签，方法如下：

   这里我们首先导入 template 这个模块，然后实例化了一个 template.Library 类，并将函数 get_recent_posts 装饰为 register.simple_tag。这样就可以在模板中使用语法 {% get_recent_posts %} 调用这个函数了。
    """
    return Post.objects.all().order_by('-createTime')[:num]
#归档模板标签

@register.simple_tag
def archives():
    """这里 dates 方法会返回一个列表，列表中的元素为每一篇文章（Post）的创建时间，且是 Python 的 date 对象，精确到月份，降序排列。接受的三个参数值表明了这些含义，一个是 created_time ，即 Post 的创建时间，month 是精度，order='DESC' 表明降序排列（即离当前越近的时间越排在前面）。例如我们写了 3 篇文章，分别发布于 2017 年 2 月 21 日、2017 年 3 月 25 日、2017 年 3 月 28 日，那么 dates 函数将返回 2017 年 3 月 和 2017 年 2 月这样一个时间列表，且降序排列，从而帮助我们实现按月归档的目的。
    """
    return Post.objects.dates('createTime', 'month', order='DESC')

@register.simple_tag
def getCategory():
    #return Category.objects.all()
    categoryList = Category.objects.annotate(num_posts=Count('post'))
    return categoryList
"""
打开 base.html，为了使用模板标签，我们首先需要在模板中导入存放这些模板标签的模块，这里是 blog_tags.py 模块。当时我们为了使用 static 模板标签时曾经导入过 {% load staticfiles %}，这次在 {% load staticfiles %} 下再导入 blog_tags：
"""