from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.views.generic.edit import FormMixin
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.core.paginator import Paginator
from django.http import HttpResponse
from django.urls import reverse_lazy, reverse

from .models import Post, Comment
from .forms import PostForm, CommentForm


# Create your views here.
"""
第一个版本，HelloWorld
"""
# def home(request):
#     return HttpResponse(
#         "<h1 style='color: blue;'>我的博客首页！</h1>"
#         "<p>欢迎来到我的Django博客</p>"
#         "<a href='/about/'>关于</a>"
#         )

# def about(request):
#     return HttpResponse(
#         "<h1> 关于开发者 </h1>"
#         "<p> 我是一名大二自动化学生，正在学习django开发</p>"
#         "<p><a href='/'>返回首页</a></p>"
        
#         )

def home(request):
    """
    home 的 Docstring
    
    :param request: 说明

    博客首页 - 显示所有文章
    """
    # 从数据库获取所有文章，按发布时间倒序排列
    posts_list = Post.objects.all().order_by('-date_posted')

    # 分页，每页显示五篇文章
    paginator = Paginator(posts_list, 5)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    # 获取当前页的文章
    posts = page_obj.object_list

    # 创建上下文数据（传递给模板的变量）
    content = {
        'posts': posts, # 文章列表
        'page_obj': page_obj,
        'title': '博客首页',    # 页面标题
    }

    # render函数：渲染模板并返回响应
    # 参数1：request对象
    # 参数2：模板文件路径
    # 参数3：上下文数据
    return render(request, 'blog/home.html', content)

def about(request):
    """
    about 的 Docstring
    
    :param request: 说明

    关于页面
    """
    # 给模板传递标题变量
    content = {'title': '关于我们'}
    return render(request, 'blog/about.html', content)
 
@login_required # 需要登陆后才能使用
def profile(request):
    """
    profile 的 Docstring
        
    :param request: 说明

    用户个人资料 - 显示该用户的所有文章
    """
    # 获取当前用户的所有文章（post_set是Django自动创建的反向关系）
    user_posts = request.user.post_set.all().order_by('-date_posted')

    content = {
        'posts': user_posts,
        'title': '个人资料',
    }
    return render(request, 'blog/profile.html', content)

def register(request):
    """
    register 的 Docstring
    
    :param request: 说明

    用户注册视图
    """
    if request.method == 'POST':
        # 处理表单请求
        form = UserCreationForm(request.POST)
        if form.is_valid():
            # 保存用户
            user = form.save() 

            # 自动登录新的用户
            login(request, user)

            # 显示成功的消息
            username = form.cleaned_data.get('username')
            messages.success(request, f'账户{username}创建成功！')
            
            # 重定向到首页
            return redirect('blog-home')
    else: 
        # 如果是get请求，显示空表单
        form = UserCreationForm()

    context = {
        'form': form, 
        'title': '用户注册'
    }
    return render(request, 'blog/register.html', context)

def handler404(request, exception):
    return render(request, 'blog/404.html', status=404)
   
# 文章详情视图
# 文章详情视图 + 评论
class PostDetailView(FormMixin, DetailView):
    model = Post
    template_name = 'blog/post_detail.html'
    context_object_name = 'post'      
    form_class = CommentForm          # 用于生成评论表单

    def get_success_url(self):
        # 评论成功后，还是回到文章详情页
        return reverse_lazy('post-detail', kwargs={'pk': self.object.pk})

    def get_context_data(self, **kwargs):
        # 基础上下文（包含 post）
        context = super().get_context_data(**kwargs)

        # 评论列表：通过 related_name='comments'
        context['comments'] = self.object.comments.all().order_by('date_posted')

        # 如果上下文里还没有 form，就生成一个空表单
        if 'form' not in context:
            context['form'] = self.get_form()

        return context

    def post(self, request, *args, **kwargs):
        # 处理评论提交
        self.object = self.get_object()

        # 未登录用户不能评论，重定向到登录页
        if not request.user.is_authenticated:
            messages.warning(request, '登录后才能发表评论哦~')
            return redirect('login')
        
        form = self.get_form()
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = self.object       # 关联到当前文章
            comment.author = request.user    # 评论者是当前用户
            comment.save()

            messages.success(request, '评论已发布！')
            return redirect(self.get_success_url())   # ✅ 调用上面的 get_success_url
        else:
            # 表单校验失败，连同错误信息一起渲染回去
            return self.render_to_response(self.get_context_data(form=form))


# 创建文章视图
class PostCreateView(LoginRequiredMixin, CreateView):
    form_class = PostForm
    template_name = 'blog/post_form.html'

    def form_valid(self, form):
        # 设置作者为当前登录用户
        form.instance.author = self.request.user
        messages.success(self.request, '文章已成功发布！')
        return super().form_valid(form)
    
    def get_success_url(self):
        return reverse_lazy('post-detail', kwargs={'pk': self.object.pk})


# 更新文章视图
class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    form_class = PostForm
    template_name = 'blog/post_form.html'

    def form_valid(self, form):
        form.instance.author = self.request.user
        messages.success(self.request, '文章已成功更新！')
        return super().form_valid(form)
    
    def test_func(self):
        # 检查当前用户是否是文章作者
        post = self.get_object()
        return self.request.user == post.author
    
    def get_success_url(self):
        return reverse_lazy('post-detail', kwargs={'pk': self.object.pk})


# 删除文章视图
class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Post
    template_name = 'blog/post_confirm_delete.html'
    success_url = reverse_lazy('blog-home')

    def test_func(self):
        # 检查当前用户是否是文章作者
        post = self.get_object()
        return self.request.user == post.author
    
    def delete(self, request, *args, **kwargs):
        messages.success(request, '文章已成功删除！')
        return super().delete(request, *args, **kwargs)


# 自动分页视图（首页列表）
class PostListView(ListView):
    model = Post
    template_name = 'blog/home.html'
    context_object_name = 'posts'   # ✅ 改成 context_object_name
    ordering = ['-date_posted']
    paginate_by = 5

