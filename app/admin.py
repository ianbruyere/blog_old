from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django import forms
from .models import *
from .forms import SignUpForm # mapMarkers, tripCost, milesTraveled, CustomUser, 
# from .forms import UserCreationForm 

class BlogAdmin(admin.ModelAdmin):
    exclude=['posted']
    prepopulated_fields = {'slug' : ('title')}

class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug':('title')}

class MapMarkerAdminForm(forms.ModelForm):
    class Meta:
        model = MapMarker
        exclude = []

class MapMarkerAdmin(admin.ModelAdmin):
    form = MapMarkerAdminForm
    list_display = ('name', 'typeOfMarker', 'submittedBy', 'alreadyVisited')

class CostAdminForm(forms.ModelForm):
    model = Cost
    exclude = []

class CostAdmin(admin.ModelAdmin):
    form = CostAdminForm
    list_display = ('cost', 'itemPurchased', 'category', 'month')

admin.site.register(MapMarker, MapMarkerAdmin)
admin.site.register(Cost, CostAdmin)
#admin.site.register(Cost)
admin.site.register(DistanceDriven)
admin.site.register(User)
admin.site.register(Hiking)
admin.site.register(Route)
# admin.site.unregister(Group)   