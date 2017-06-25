from django.db import models
from django.template.defaultfilters import slugify
from django.db.models import permalink
from random import random
from django.urls import reverse

class Tag(models.Model):
    tagName = models.CharField(max_length=120)
    slug = models.SlugField()
    
    def __str__(self):
        return self.tagName


class Photo(models.Model):
    title = models.CharField(max_length=256)
    caption = models.TextField(blank=True)
    slug = models.SlugField(max_length=250,
                            unique=True,
                          help_text=("A 'slug' is a unique URL-friendly title for an object."),
                          default=None)
    date_added = models.DateTimeField(auto_now_add=True)
    image = models.ImageField(upload_to='photos/%Y/%m')
    is_cover_photo = models.BooleanField(default=False)
    tags = models.ManyToManyField(Tag, blank=True)

    def __str__(self):
        return 'Photo: {}'.format(self.title)

    def save(self, *args, **kwargs):
        if self.slug is None:
            self.slug = slugify(self.title)
        super(Photo, self).save(*args, **kwargs)

    def get_previous_in_album(self, album):
        """Find the neighbour of this photo in the supplied gallery."""
        photos = album.photos()
        if self not in photos:
            raise ValueError('Photo does not belong to gallery.')
        previous = None
        for photo in photos:
            if photo == self:
                return previous
            previous = photo

    def get_next_in_album(self, album):
        """Find the neighbour of this photo in the supplied gallery."""

        photos = album.photos()
        if self not in photos:
            raise ValueError('Photo does not belong to gallery.')
        matched = False
        for photo in photos:
            if matched:
                return photo
            if photo == self:
                matched = True
        return None

    def get_absolute_url(self):
        return reverse('view_photo', args=[self.slug])

    def admin_thumbnail(self):

        return u'<img src="%s" width="%s", height="%s">' % \
                    (self.image.url, 200,200)
    admin_thumbnail.short_description = ('Thumbnail')
    admin_thumbnail.allow_tags = True


class Album(models.Model):
    title = models.CharField(
                             max_length=250,
                             unique=True)
    slug = models.SlugField(
                            unique=True,
                            max_length=250,
                            help_text=('A "slug" is a unique URL-friendly title for an object.'))
    description = models.TextField(
                                   blank=True)
    photos = models.ManyToManyField(Photo,
                                    related_name='albums',
                                    blank=True)
    date_added=models.DateTimeField(auto_now=True)
    class Meta:
        ordering = ['-date_added']

    @permalink
    def get_absolute_url(self):
         return ('view_album', None, {'slug' : self.slug})

    def __str__(self):
        return 'Album: {}'.format(self.title)

    def sample(self, count=4):
        """Return a sampling of the album, for use in jumbotron
        and as random album cover photos
        """
        if count > self.photo_count():
            count = self.photo_count()

        photo_set = self.photos
        return random.sample(set(photo_set), count)

    def photo_count(self):
        """Return a count of all photos in album
        """
        return self.photos.count()

    




