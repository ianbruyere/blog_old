from django.db import models
from django.db.models import permalink
from django.template.defaultfilters import slugify

# Create your models here.



class BlogPost(models.Model):
     title = models.CharField(max_length=250, unique=True)
     slug = models.SlugField(max_length=100, unique=True)
     body = models.TextField()
     author = models.CharField(max_length=100, blank=True) 
     datePosted = models.DateField(db_index=True, auto_now_add=True)
     categories = models.ManyToManyField('Category', 
                                  blank=True, default=None)

     def __str__(self):
         return 'BlogPost: {}'.format(self.title)

     def __unicode__(self):
         return '%s' % self.title

     def save(self, *args, **kwargs):
         if self.slug is None:
             self.slug = slugify(self.title)
         super(BlogPost, self).save(*args, **kwargs)


     @permalink
     def get_absolute_url(self):
         return ('view_blog_post', None, {'slug' : self.slug})

class Category(models.Model):
    title = models.CharField(max_length=100, db_index=True)
    slug = models.SlugField(max_length=100, db_index=True)

    class Meta:
        verbose_name_plural = 'Categories'

    def __unicode__(self):
        return '%s' % self.title

    @permalink
    def get_absolute_url(self):
        return ('view_blog_category', None, {'slug' : self.slug})

    def __str__(self):
        return '{}'.format(self.title)