"""
Definition of views.
"""

from django.shortcuts import render, render_to_response, get_object_or_404
from django.http import HttpRequest
from django.template import RequestContext
from datetime import datetime
from .forms import *
from django.contrib.auth import login, authenticate
from django.http.response import HttpResponseRedirect
import json
from django.core import serializers
from django.views.generic import list
from app.models import BlogPost, Category, Album, Photo

def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('home')
    else:
        form = SignUpForm()

    return render(request, 'app/signup.html', {'form' : form,
                                               'title': 'Sign Up',})

def home(request):
    """Renders the home page."""
    assert isinstance(request, HttpRequest)
    return render(
        request,
        'app/index.html',
        {
            'title':'Home Page',
            'year':datetime.now().year,
            'images': Photo.objects.filter(is_cover_photo=True).order_by('date_created')[:4],
            'posts' : BlogPost.objects.all()[:8]
        }
    )

def blogMainPage(request):
    return render(request, 
                  'blogs/blogMainPage.html',
                  {
                      'posts' : BlogPost.objects.all()
                  }
                )

def view_blog_post(request, slug):
    blogPost = get_object_or_404(BlogPost, slug=slug)
    return render(request,
                  'blogs/view_blog_post.html',
          {
           'post' : blogPost,
           'category' : Category.objects.filter(id=blogPost.category.id)
           })

def view_category(request, slug):
    category = get_object_or_404(Category, slug=slug)
    return render(request,
        'category/view_blog_category.html', {
        'category' : category,
        'posts' : BlogPost.objects.filter(category=category)[:5]
        })

def view_album(request, slug):
    album = get_object_or_404(Album, slug=slug)

    return render(request,
                  'Albums/view_album.html', {
                  'album' : album,
                  'photos' :  Photo.objects.filter(album=album),
        })

def contact(request):
    """Renders the contact page."""
    assert isinstance(request, HttpRequest)
    return render(
        request,
        'app/contact.html',
        {
            'title':'Contact',
            'message':'Your contact page.',
            'year':datetime.now().year,
        }
    )

def about(request):
    """Renders the about page."""
    assert isinstance(request, HttpRequest)
    return render(
        request,
        'app/about.html',
        {
            'title':'About Minor Interactions',
            # 'message':'Your application description page.',
            'year':datetime.now().year,
        }
    )

def tripoutline(request):
    # if this a POST request we need to process form data
    if request.method == 'POST':
        mapMarkersForm = MapMarkersForm(request.POST)
        if mapMarkersForm.is_valid():
            markers = mapMarkersForm.save()
            # process the data in form.cleaned_data as required

            return HttpResponseRedirect('tripoutline')
    # if GET or other method return a blank form
    else:
        mapMarkersForm = MapMarkersForm()
    from app.models import MapMarker
    """Renders the trip outline page"""
    assert isinstance(request, HttpRequest)

    # this lets me separate the javascript out to its own file
    markers_json = serializers.serialize('json', MapMarker.objects.all())
    return render(
        request,
        'app/tripoutline.html',
        {
         'title': 'Trip',
         'message': 'Where I want to go and Where I have been',
         'year': datetime.now().year,
         'markers_json' : markers_json,
         'mapMarkersForm' : mapMarkersForm
         }

     )

def bythenumbers(request):
    from app.models import Cost, DistanceDriven, Hiking, Route
    assert isinstance(request, HttpRequest)
    money_json = serializers.serialize('json', Cost.objects.all())
    distance_json = serializers.serialize('json',DistanceDriven.objects.all())
    climbs = serializers.serialize('json', Route.objects.all())
    hikes = serializers.serialize('json', Hiking.objects.all())
    return render(
        request,
        'app/bythenumbers.html',
        {
            'title' : 'By The Numbers',
            'money' : money_json,
            'distance' : distance_json,
            'climbs' : climbs,
            'hikes' : hikes,
            })

def photos(request):
    from app.models import Photo, Album
    assert isinstance(request, HttpRequest)
    albums = Album.objects.all()
    return render(
        request,
        'app/photos.html', {
            'title' : 'Gallery',
            'photos' : Photo.objects.filter(is_cover_photo=True),
            'albums' : albums
            }
        )






