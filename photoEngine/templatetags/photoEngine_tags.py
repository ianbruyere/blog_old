import random
from django import template
from ..models import Album
from ..models import Photo

register = template.Library()

@register.inclusion_tag('next_in_album.html')
def next_in_album(photo, album):
    return {'photo' : photo.get_next_in_album(album)}

@register.inclusion_tag('prev_in_album.html')
def previous_in_gallery(photo, album):
    return {'photo' : photo.get_previous_in_album(album)}