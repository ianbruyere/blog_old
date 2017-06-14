import zipfile
from zipfile import BadZipFile
from PIL import Image
from django import forms
from .models import *
from django.contrib import messages
import os
from io import BytesIO
from django.core.files.base import ContentFile
import logging
from django.conf import settings
from django.template.defaultfilters import slugify

class UploadZipForm(forms.Form):
    zip_file = forms.FileField()

    title = forms.CharField(
                            max_length=250,
                            required=False,
                            help_text=("All uploaded photos will be given a title made up of this title + a "
                                        "sequential number. <br>This field is required if creating a new "
                                        "gallery, but is optional when adding to an exisiting album - if "
                                        "not supplied, the photo titles will be creating from the existing "
                                        "gallery name."))
    album = forms.ModelChoiceField(Album.objects.all(),
                                   required=False,
                                   help_text = ("Select a album to add these images to. Leave this empty to "
                                                "create a new gallery from the supplied title"))
    caption = forms.CharField(required=False,
                              help_text=("Caption will be added to all photos"))

    def clean_zip_file(self):
        """Open the zip file a first time, to check that it is a valid zip archive.
        We will open it again in a moment, so we have some duplication, but let's focus
        on keeping it easier to read!"""

        zip_file = self.cleaned_data['zip_file']
        try:
            zip = zipfile.ZipFile(zip_file)
        except BadZipFile as e:
            raise forms.ValidationError(str(e))
        bad_file = zip.testzip()
        if bad_file:
            zip.close()
            raise forms.ValidationError("'%s' in the .zip archive is corrupt." % bad_file)
        zip.close() # close file in all cases
        return zip_file

    def clean_title(self):
        title = self.cleaned_data['title']
        if title and Album.objects.filter(title=title).exists():
            raise forms.ValidationError('An album with that title already exists.')
        return title

    def clean(self):
        cleaned_data = super(UploadZipForm, self).clean()
        if not self['title'].errors:
            # If there is already an error in the tile, no need to add another
            # error related to the same field
            if not cleaned_data.get('title', None) and not cleaned_data['album']:
                raise forms.ValidationError('Select an existing album, or enter a title for a new album.')
        return cleaned_data

    def save(self, request=None, zip_file=None):
        if not zip_file:
            zip_file = self.cleaned_data['zip_file']
        zip = zipfile.ZipFile(zip_file)
        count = 1
        if self.cleaned_data['album']:
            album = self.cleaned_data['album']
        else:
            album = Album.objects.create(title=self.cleaned_data['title'],
                                         slug=slugify(self.cleaned_data['title']),
                                         description=self.cleaned_data['description'])
        for filename in sorted(zip.namelist()):
            if filename.startswith('__') or filename.startswith('.'):
                continue

            if os.path.dirname(filename): 
                # this checks if one of the files is instead a directory
                if request:
                    messages.warning(request, ('Ignoring file "{filename}" as it is in a subfolder; all images should be in the top folder of the zip.').format(filename=filename),
                                     fail_silently=False)
                    
                continue
            data = zip.read(filename)

            if not len(data):
                continue

            photo_title_root = self.cleaned_data['title'] if self.cleaned_data['title'] else album.title

            photo = Photo(title=photo_title_root,
                          caption=self.cleaned_data['caption']
                          )

            # Basic check tha we have a valid image
            try:
                file = BytesIO(data)
                opened = Image.open(file)
                opened.verify()
            except Exception:
                # PIL does not recognize as an image
                logger.error('Could not process file "{0}" in the .zip archive.'.format(
                    filename))
                continue
            
            contentfile = ContentFile(data)
            photo.image.save(filename, contentfile)
            photo.save()
            album.photos.add(photo)
            count += 1
        
        zip.close()

        if request:
            messages.success(request,
                             ('The photos have been added to the album'),
                             fail_silently=True)

        

                                          
