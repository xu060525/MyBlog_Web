# blog/forms.py
from django import forms
from .models import Post, Comment

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'content']  # 在这里定义一次
        
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