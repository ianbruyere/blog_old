from django.contrib import admin
from django import forms
from redactor.widgets import RedactorEditor
from .models import *
# Register your models here.

admin.site.register(Category)

class EntryAdminForm(forms.ModelForm):
    class Meta:
        model = BlogPost
        exclude = []
        widgets = {
            'body' : RedactorEditor()
            }

class EntryAdmin(admin.ModelAdmin):
    form = EntryAdminForm


admin.site.register(BlogPost, EntryAdmin)