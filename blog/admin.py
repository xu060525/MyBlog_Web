from django.contrib import admin
from .models import Post, Comment

# Register your models here.

# 简单注册
# admin.site.register(Post)
# admin.site.register(Comment)

# 装饰器注册
@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    """
    PostAdmin 的 Docstring

    文章管理配置
    """
    # 列表页显示的字段
    list_display = ('title', 'author', 'date_posted', 'comment_count')

    # 右侧过滤器
    list_filter = ('date_posted', 'author')

    # 搜索框
    search_fields = ('title', 'content')

    # 日期层级导航
    date_hierarchy = 'date_posted'

    # 每页显示数量
    list_per_page = 20

    def comment_count(self, obj):
        """
        comment_count 的 Docstring
        
        :param self: 说明
        :param obj: 说明

        自定义列：显示评论数量
        """
        return obj.comments.count()
    comment_count.short_description = '评论数'  # 列标题

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    """
    CommentAdmin 的 Docstring

    评论管理配置
    """
    # 列表页显示：评论预览、作者、文章、时间
    list_display = ('content_preview', 'author', 'post', 'date_posted')

    # 过滤器
    list_filter = ('date_posted', 'author')

    # 搜索
    search_fields = ('content',)

    # 每页显示数量
    list_per_page = 30

    def content_preview(self, obj):
        """
        content_preview 的 Docstring
        
        :param self: 说明
        :param obj: 说明

        评论内容预览
        """
        if len(obj.content) > 50:
            return obj.content[:50] + '...'
        return obj.content
    content_preview.short_description = '评论内容'