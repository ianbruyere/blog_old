"""
Definition of models.
"""

from django.db import models
from django.db.models import permalink
from django.core.validators import RegexValidator
from django.contrib.auth.models import User, AbstractUser

alphanumeric = RegexValidator(r'^[0-9a-zA-Z]*$', 'Only alphanumeric characters are allowed.')
# Create your models here.
class User(AbstractUser):
    is_authorized = models.BooleanField(default=False)

class MapMarker(models.Model):
    name = models.CharField(max_length=60)
    address = models.CharField(max_length=80, default=None)
    lat = models.DecimalField(max_digits=10, decimal_places=6, default=None)
    lng = models.DecimalField(max_digits=10, decimal_places=6, default=None )
    partOfTrip = models.IntegerField(default=0, null=True)
    orderVisiting = models.IntegerField(default=0, null=True)
    typeOfMarker = models.CharField(max_length=70, choices=(("Climbing", "Climbing"), ("Entertainment", "Entertainment"), ("Food", "Food"), ("Meet-Up", "Meet-Up")), default='Climbing')
    description = models.TextField(max_length=1000, default=None, null=True)
    confirmed = models.BooleanField(default=False, blank=True)
    date = models.DateField(default=None, null=True)
    alreadyVisited = models.BooleanField(default=False)

    def __str__(self):
        return 'MapMarker: {}'.format(self.name)

# keeps track of how the trip has cost me and what categories it falls in
class Cost(models.Model):
    cost = models.DecimalField(max_digits=10, decimal_places=2)
    itemPurchased = models.CharField(max_length=100, default='Food')
    category = models.CharField(max_length=40, choices=(('Gas', 'Gas'), ('Food', 'Food'), ('Entertainment', 'Entertainment'), ('Misc', 'Misc'), ('Camping', 'Camping'), ('Hiking', 'Hiking')), default='Climbing')
    state = models.CharField(max_length=2)
    city = models.CharField(max_length=40)
    month = models.CharField(max_length=40, default='May')

## this will keep track of how many miles I have gone, by what point, and at what time
## maybe eventually have something that says how long it has been since I have been on the road
## in days and whatnot
class DistanceDriven(models.Model):
    cumulativeMilesTraveled = models.DecimalField(max_digits=12, decimal_places=2)
    checkInPointPlace = models.CharField(max_length=100)
    state= models.CharField(max_length=2)
    date = models.DateField()

class Route(models.Model):
    name = models.CharField(max_length=100)
    location = models.CharField(max_length=256)
    grade = models.CharField(max_length=100)
    sendStatus = models.CharField(max_length=100) # this can also be number of attempts
    date = models.DateField()
    belayer = models.CharField(max_length=100) # belayer at time of send
    betaSpew = models.TextField() # anythin I want to say, form how well liked the route was to actual beta
                                  # though beta should probably be hidden by spoilers
class Hiking(models.Model):
    name = models.CharField(max_length=60)
    location = models.CharField(max_length=60)
    distance = models.CharField(max_length=60)
    numberOfDays = models.IntegerField()
    typeOfTerrain = models.CharField(max_length=60, choices=(('Hilly', 'Hilly'), ('Flat', 'Flat'), ('Mixed', 'Mixed')))


class BlogPost(models.Model):
     title = models.CharField(max_length=250, unique=True)
     slug = models.SlugField(max_length=100, unique=True)
     body = models.TextField() 
     datePosted = models.DateField(db_index=True, auto_now_add=True)
     category = models.ForeignKey('Category')

     def __str__(self):
         return 'BlogPost: {}'.format(self.title)

     def __unicode__(self):
         return '%s' % self.title

     @permalink
     def get_absolute_url(self):
         return ('view_blog_post', None, {'slug' : self.slug})





class Category(models.Model):
    title = models.CharField(max_length=100, db_index=True)
    slug = models.SlugField(max_length=100, db_index=True)

    def __unicode__(self):
        return '%s' % self.title

    @permalink
    def get_absolute_url(self):
        return ('view_blog_category', None, {'slug' : self.slug})

    def __str__(self):
        return 'Category: {}'.format(self.title)


