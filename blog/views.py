from django.shortcuts import render,get_object_or_404
from blog.models import Post,Comment
from django.core.paginator import Paginator
from django.db.models import Count , Q

# Create your views here.
def blog_home(request):
    all_posts = (
        Post.objects.filter(status=True)
        .select_related('author', 'category')
        .annotate(approved_comments=Count('comment', filter=Q(comment__approved=True)))
    )
    paginator=Paginator(all_posts,2)
    page_number=request.GET.get('page')
    page_obj=paginator.get_page(page_number)
    context={'page_obj':page_obj}
    return render(request,"blog/blog-home.html",context)

def blog_single(request,pk):
    post=get_object_or_404(Post,status=True,pk=pk)
    comments=Comment.objects.filter(post=post.id)
    context={'post':post,'comments':comments}
    return render(request,"blog/blog-single.html",context)

