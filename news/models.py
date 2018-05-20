
from django.db import models
from django.contrib.auth.models import User
from django.utils.six import python_2_unicode_compatible
from django.urls import reverse
import markdown
from django.utils.html import strip_tags
# Create your models here.

#python_2_unicode_compatible 装饰器用于兼容python2
#分类
@python_2_unicode_compatible
class Category(models.Model):

    '''
        Django 要求模型必须继承models.Model类。
        Django 内置的全部类型可查看文档：
        https: // docs.djangoproject.com / en / 1.10 / ref / models / fields / # field-types
    '''
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

#标签
@python_2_unicode_compatible
class Tag(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name



class Imgage(models.Model):
    Img = models.ImageField()

    def _str_(self):
        return self.Img


#文章
@python_2_unicode_compatible
class Post(models.Model):
    title = models.CharField(max_length=70)
    body = models.TextField()

    #下去试试 models.TimeField()

    created_time = models.DateTimeField(auto_now_add=True)
    modified_time = models.DateTimeField()

    #摘要，允许空值
    excerpt = models.CharField(max_length=200, blank=True)

    views = models.PositiveIntegerField(default=0)

    '''
    这里的分类与标签，和上面定义过的不一样，这里是把文章对应的分类与标签对应关联起来
    规定：①一篇文章只能有一个分类，但是一个分类中可以有多篇文章，用外键关联
         ②一篇文章可以用多个标签，一个标签下也可以有多篇文章，用ManyToManyField()关联
         ③文章可以没有标签
    '''
    category = models.ForeignKey(Category)
    tags = models.ManyToManyField(Tag, blank=True)

    author = models.ForeignKey(User)
    img = models.ManyToManyField(Imgage)

    def __str__(self):

        return self.title

    def get_absolute_url(self):
        return reverse('news:post_detail',kwargs = {'pk': self.pk})

    class Meta:
        ordering = ["-created_time"]

    def increase_views(self):
        self.views +=1
        self.save(update_fields=['views'])

    def save(self, *args, **kwargs):
        if not self.excerpt:
            md = markdown.Markdown(extensions=[
                'markdown.extensions.extra',
                'markdown.extensions.codehilite',
            ])

            #先将markdown文本渲染成HTML文本，然后用strip_tags去掉HTML文本的全部HTML标签（为了防止文本中含有标签弄坏排版）
            #抽取前60个字符给excerpt
            self.excerpt = strip_tags(md.convert(self.body))[:60]

        #调用父类的save方法将数据保存到数据库中
        super(Post,self).save(*args, **kwargs)
