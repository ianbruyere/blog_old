from django.contrib import admin
from django import forms
from .models import *
from .forms import UploadZipForm
from django.shortcuts import render
from django.conf.urls import url
from django.contrib.admin import helpers
from django.http import HttpResponseRedirect

# Register your models here.
#admin.site.register(Photo)
admin.site.register(Album)
admin.site.register(Tag)

class PhotoAdminForm(forms.ModelForm):
    class Meta:
        model = Photo
        exclude = []

class PhotoAdmin(admin.ModelAdmin):
    form = PhotoAdminForm
    list_display = ('title', 'admin_thumbnail')

    def get_urls(self):
        urls = super(PhotoAdmin, self).get_urls()
        custom_urls = [
            url(r'^upload_zip/$',
                self.admin_site.admin_view(self.upload_zip),
                name='upload_zip')
        ]
        return custom_urls + urls

    def upload_zip(self, request):

        context = {
            'title': ('Upload a zip archive of photos'),
            'app_label': self.model._meta.app_label,
            'opts': self.model._meta,
            'has_change_permission': self.has_change_permission(request)
            }

        if request.method == 'POST':
            form = UploadZipForm(request.POST, request.FILES)
            if form.is_valid():
                form.save(request=request)
                return HttpResponseRedirect('..')
        else:
            form = UploadZipForm()

        context['form'] = form
        context['adminform'] = helpers.AdminForm(form,
                                                 list([(None, {'fields': form.base_fields})]),
                                                 {})
        return render(request, 'admin/photoEngine/photo/upload_zip.html', context)

admin.site.register(Photo, PhotoAdmin)