from django.shortcuts import render, render_to_response, get_object_or_404
from .models import *
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

# Create your views here.
def blogMainPage(request):
    blog_posts = BlogPost.objects.all()
    page = request.GET.get('page', 1)

    paginator = Paginator(blog_posts, 12)
    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        posts = paginator.page(1)
    except EmptyPage:
        posts = paginator.page(paginator.num_pages)
    return render(request, 
                  'blogMainPage.html',
                  {
                      'posts' : posts
                      
                  }
                )

def view_blog_post(request, slug):
    blogPost = get_object_or_404(BlogPost, slug=slug)
    return render(request,
                  'view_blog_post.html',
          {
           'post' : blogPost,
           'categories' : blogPost.categories.all()
           })

def view_category(request, slug):
    category = get_object_or_404(Category, slug=slug)
    return render(request,
        'view_blog_category.html', {
        'category' : category,
        'posts' : BlogPost.objects.filter(categories=category)
        })

#def blog_grid_view(request, number_of_posts=None, paginate=False):
#    if number_of_posts == None:
#        blogPosts = BlogPost.objects.all()
#    else:
#        blogPosts = BlogPost.objects.all()[:number_of_posts]
#    if paginate:
#        blogPosts = paginateBlogPosts(blogPosts)
#    return render(request, 
#                  'blog_grid_view',
#                  {
#                      'posts' : blogPosts
#                  }
#                )

#def paginateBlogPosts(list_posts):
#    page = request.GET.get('page', 1)

#    paginator = Paginator(list_posts, 12)
#    try:
#        paginated_posts = paginator.page(page)
#    except PageNotAnInteger:
#        paginated_posts = paginator.page(1)
#    except EmptyPage:
#        paginated_posts = paginator.page(paginator.num_pages)

#    return paginated_posts