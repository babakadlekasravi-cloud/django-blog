from django import template
from blog.models import Post,Comment

register=template.Library()
@register.simple_tag(name='comments_count')
def comments_tag(pid):
    post=Post.objects.get(pk=pid)
    return Comment.objects.filter(post=post,approved=True).count()

