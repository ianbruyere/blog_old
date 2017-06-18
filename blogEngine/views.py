from django.shortcuts import render, render_to_response, get_object_or_404
from .models import *

# Create your views here.
def blogMainPage(request):
    return render(request, 
                  'blogMainPage.html',
                  {
                      'posts' : BlogPost.objects.all()
                      
                  }
                )

def view_blog_post(request, slug):
    blogPost = get_object_or_404(BlogPost, slug=slug)
    return render(request,
                  'view_blog_post.html',
          {
           'post' : blogPost,
           })

def view_category(request, slug):
    category = get_object_or_404(Category, slug=slug)
    return render(request,
        'view_blog_category.html', {
        'category' : category,
        'posts' : BlogPost.objects.filter(category=category)[:5]
        })

def blog_grid_view(request):
    return render(request, 
                  'blog_grid_view',
                  {
                      'posts' : BlogPost.objects.all()    
                  }
                )