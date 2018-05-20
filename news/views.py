#coding=utf-8
from django.shortcuts import render, get_object_or_404
import markdown
# Create your views here.

from django.http import HttpResponse
from .models import Post, Category, Tag, Imgage
from django.views.generic import ListView, DetailView
from markdown.extensions.toc import TocExtension
from django.utils.text import slugify
from django.db.models import Q


# Create your views here.

# def index(request):
#   #  return HttpResponse("hello!")
#     return render(request, 'news/index.html', context={
#                         'title': '欢迎',
#                         'welcome': '欢迎访问本新闻网站！',
#                     }
#                   )
class IndexView(ListView):
    model = Post

    template_name = 'news/index.html'

    context_object_name = 'post_list'

    def get_context_data(self, **kwargs):
        # 覆写该方法，以便我们获得自定义的模板变量

        context = super(IndexView, self).get_context_data(**kwargs)

        # 父类生成的字典中已有 paginator、page_obj、is_paginated 这三个模板变量，
        # paginator 是 Paginator 的一个实例，
        # page_obj 是 Page 的一个实例，
        # is_paginated 是一个布尔变量，用于指示是否已分页。
        # 例如如果规定每页 10 个数据，而本身只有 5 个数据，其实就用不着分页，此时 is_paginated=False。
        # 由于 context 是一个字典，所以调用 get 方法从中取出某个键对应的值。
        paginator = context.get('paginator')
        page = context.get('page_obj')
        is_paginated = context.get('is_paginated')

        pagination_data = self.pagination_data(paginator, page, is_paginated)
        context.update(pagination_data)
        return context

    def pagination_data(self, paginator, page, is_paginated):
        if not is_paginated:
            return {}

        left = []
        right = []

        left_has_more = False
        right_has_more = False
        first = False
        last = False

        page_number = page.number
        total_pages = paginator.num_pages

        # 获得整个分页的页码列表
        page_range = list(paginator.page_range)

        if page_number == 1:
            #            right = page_range[page_number:page_number + 1]
            right = page_range[page_number:page_number + 1]

            if right[-1] < total_pages - 1:
                right_has_more = True

            if right[-1] < total_pages:
                last = True
        elif page_number == total_pages:
            left = page_range[(page_number - 3) if (page_number - 3) > 0 else 0:page_number - 1]

            if left[0] > 2:
                left_has_more = True
            if left[0] > 1:
                first = True

        else:
            left = page_range[(page_number - 3) if (page_number - 3) > 0 else 0: page_number - 1]
            right = page_range[page_number:page_number + 1]

            if right[-1] < total_pages - 1:
                right_has_more = True
            if right[-1] < total_pages:
                last = True

            if left[0] > 2:
                left_has_more = True
            if left[0] > 1:
                first = True

        data = {
            'left': left,
            'right': right,
            'left_has_more': left_has_more,
            'right_has_more': right_has_more,
            'last': last,
            'first': first,
        }

        return data

# class CategoryView(ListView):
#     model = Post
#     template_name = 'news/index.html'
#     context_object_name = 'post_list'
#
#     def get_queryset(self):
#         cate = get_object_or_404(Category, pk=self.kwargs.get('pk'))
#         return super(CategoryView, self).get_queryset().filter(category=cate)

def category(request, pk):
    # 记得在开始部分导入 Category 类
    cate = get_object_or_404(Category, pk=pk)
    post_list = Post.objects.filter(category=cate).order_by('-created_time')
    return render(request, 'news/category_detail.html', context={'post_list': post_list})


