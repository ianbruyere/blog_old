from django.shortcuts import render
from .models import *
from django.shortcuts import render, render_to_response, get_object_or_404
from django.http import HttpRequest

def photos(request):
    assert isinstance(request, HttpRequest)
    albums = Album.objects.all()

    return render(
        request,
        'photos.html', {
            'title' : 'Gallery',
            'albums' : albums
            }
        )

def view_album(request, slug):
    album = get_object_or_404(Album, slug=slug)

    return render(request,
                  'view_album.html', {
                  'album' : album.photos.all(),

        })

def view_photo(request, slug):
    photo = get_object_or_404(Photo, slug=slug)
    album = Album.objects.filter(photos=photo)

    return render(request,
                  'view_photo.html', {
                      'photo': photo,
                      'album' : album
                      })