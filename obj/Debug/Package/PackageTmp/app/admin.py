from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import *
from .forms import SignUpForm # mapMarkers, tripCost, milesTraveled, CustomUser, 
# from .forms import UserCreationForm 

class BlogAdmin(admin.ModelAdmin):
    exclude=['posted']
    prepopulated_fields = {'slug' : ('title')}

class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug':('title')}

admin.site.register(Photo)
admin.site.register(Album)
admin.site.register(MapMarker)
admin.site.register(Cost)
admin.site.register(DistanceDriven)
admin.site.register(User)
admin.site.register(BlogPost)
admin.site.register(Category)
admin.site.register(Hiking)
admin.site.register(Route)
# admin.site.unregister(Group)   