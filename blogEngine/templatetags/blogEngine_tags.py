from django import template 
from blogEngine.models import BlogPost
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

register = template.Library()


class BlogPostsNode(template.Node):
    def __init__(self, numberRequested):
        self.num = numberRequested
    def getRequestedNumberOfPosts(self):
        if self.num == 0:
            return BlogPost.objects.all()
        else:
            return BlogPost.objects.all()[:self.num]
    def getBlogPostsFilterByCategory(category):
        return BlogPost.objects.filter(category=category)

@register.inclusion_tag('blogEngine/blog_grid_view.html', takes_context=True)
def getBlogGridView(context, numberRequested, paginate=False):
    request = context['request']
    blogPosts = BlogPostsNode(numberRequested).getRequestedNumberOfPosts()
    if paginate:
        page = request.GET.get('page', 1)
        paginator = Paginator(blogPosts, 12)
        try:
            blogPosts = paginator.page(page)
        except PageNotAnInteger:
            blogPosts = paginator.page(1)
        except EmptyPage:
            blogPosts = paginator.page(paginator.num_pages)

    return {'posts': blogPosts}



    