from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from django.utils import timezone
from django.utils.text import slugify

# Create your models here.

class Category(models.Model):
    """
    Category 的 Docstring

    文章分类，比如：Python、Django、生活随笔
    """
    name = models.CharField('分类名称', max_length=50, unique=True)
    slug = models.SlugField('URL别名', max_length=50, unique=True)
    created_at = models.DateTimeField('创建时间', auto_now_add=True)

    class Meta:
        verbose_name = '分类'
        verbose_name_plural = '分类'
        ordering = ['name']

    def __str__(self):
        return self.name
    
    def get_absolute_url(self):
        # 以后可以做的分类筛选项
        return reverse('blog-category', kwargs={'slug': self.slug})
    
class Tag(models.Model):
    """
    Tag 的 Docstring

    文章标签，比如：入门、进阶、心得、bug记录
    """
    name = models.CharField('标签名称', max_length=30, unique=True)
    slug = models.SlugField('URL别名', max_length=30, unique=True)
    created_at = models.DateTimeField('创建时间', auto_now_add=True)

    class Meta:
        verbose_name = '标签'
        verbose_name_plural = '标签'
        ordering = ['name']

    def __str__(self):
        return self.name
    
    def get_absolute_url(self):
        # 以后可以做标签筛选页，如 /tag/python/
        return reverse('blog-tag', kwargs={'slug': self.slug})
    
class Post(models.Model):
    """
    Blog 文章模型
    这个类定义了文章的数据结构
    """

    # CharField: 短文本字段，比如标题
    title = models.CharField('标题', max_length=200)

    # TextField: 长文本字段，比如文章内容
    content = models.TextField('内容')

    # 分类（可为空）
    category = models.ForeignKey(
        Category, 
        verbose_name='分类', 
        null=True, 
        blank=True, 
        on_delete=models.SET_NULL, 
        related_name='posts'
    )
    
    # 标签（多对多，可对空）
    tags = models.ManyToManyField(
        Tag, 
        verbose_name='标签',
        blank=True, 
        related_name='posts'
    )

    # DateTimeField: 日期时间字段
    # auto_now_add=True: 创建时自动设置当前时间
    date_posted = models.DateTimeField('发布时间', default=timezone.now)

    # ForeignKey: 外键，关联 User 模型
    # on_delete=models.CASCADE: 如果用户被删除，他的文章也被删除
    author = models.ForeignKey(User, verbose_name='作者', on_delete=models.CASCADE)

    def __str__(self):
        """
        __str__ 的 Docstring
        
        :param self: 说明

        在 Admin 后台和 Shell 中显示的字符串
        比如: 显示文章标题而不是 "Post object (1)"
        """
        return self.title
    
    def get_absolute_url(self):
        """
        get_absolute_url 的 Docstring
        
        :param self: 说明

        返回文章详情页的 URL
        用于创建文章后自动跳转
        """
        return reverse('post-detail', kwargs={'pk': self.pk})
    
class Comment(models.Model):
    """
    Comment 的 Docstring

    文章评论模型
    每个评论属于一篇文章和一个用户
    """
    # 评论属于哪篇文章
    post = models.ForeignKey(
        Post,
        verbose_name='文章',
        related_name='comments',    # 可以通过 post.comments 访问所有评论
        on_delete=models.CASCADE
    )

    # 评论者是谁
    author = models.ForeignKey(User, verbose_name='评论者', on_delete=models.CASCADE)

    # 评论内容
    content = models.TextField('评论内容')

    # 评论时间
    date_posted = models.DateTimeField('评论时间', auto_now_add=True)

    def __str__(self):
        """
        __str__ 的 Docstring

        :param self: 说明

        显示谁评论了哪篇文章
        例如：“张三 评论了 Python入门教程
        """
        return f'{self.author.username} 评论了 {self.post.title}'
    
    class Meta:
        """
        Meta 的 Docstring

        模型的元数据配置
        """
        ordering = ['date_posted']   # 按评论时间正序排列（从早到晚）
