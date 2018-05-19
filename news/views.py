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