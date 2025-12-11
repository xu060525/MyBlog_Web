# blog/forms.py
from django import forms
from .models import Post, Comment, Category, Tag

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'content', 'category', 'tags']  # 在这里定义一次
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': '请输入文章标题', 
            }), 
            'content': forms.Textarea(attrs={
                'class': 'form-control', 
                'rows': 10, 
                'placeholder': '请输入文章内容'
            }), 
            'category': forms.Select(attrs={
                'class': 'form-select',
            }),
            'tags': forms.SelectMultiple(attrs={
                'class': 'form-select', 
            }),
        }
        labels = {
            'title': '标题',
            'content': '正文内容',
            'category': '分类', 
            'tags': '标签', 
        }
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['title'].widget.attrs.update({'class': 'form-control'})
        self.fields['content'].widget.attrs.update({'class': 'form-control', 'rows': 15})

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['content']    # 只让用户填写评论内容

        widgets = {
            'content': forms.Textarea(attrs={
                'class': 'form-control', 
                'rows': 3, 
                'placeholder': '写下你的评论...'
            })
        }
        labels = {
            'content': '评论内容',
        }