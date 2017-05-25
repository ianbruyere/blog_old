"""
Definition of forms.
"""

from django import forms
from django.contrib.auth.forms import AuthenticationForm, ReadOnlyPasswordHashField, UserCreationForm
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth import authenticate
from django.utils.translation import ugettext_lazy as _
from django.core.validators import RegexValidator
from app.customAuthentication import MyBackEnd
from app.models import  MapMarker, User
from django.forms import ModelForm

alphanumeric = RegexValidator(r'^[0-9a-zA-Z]*$', 'Only alphanumeric characters are allowed.')


class BootstrapAuthenticationForm(AuthenticationForm):
    """Authentication form which uses boostrap CSS."""
    username = forms.CharField(max_length=254,
                               widget=forms.TextInput({
                                   'class': 'form-control',
                                   'placeholder': 'User name'}))
    password = forms.CharField(label=_("Password"),
                               widget=forms.PasswordInput({
                                   'class': 'form-control',
                                   'placeholder':'Password'}))

class SignUpForm(UserCreationForm):
    email = forms.EmailField(max_length=260, help_text='Required')
    def clean_username(self):
        username = self.cleaned_data['username'] 
        try:
            User._default_manager.get(username=username)
        except User.DoesNotExist:
            return username
        raise forms.ValidationError(self.error_messages['duplicate_username'])

    class Meta(UserCreationForm.Meta):
        model = User
        fields = ('email', 'username', 'first_name', 'last_name', 'password1', 'password2')

class MapMarkersForm(ModelForm):
    class Meta:
        model = MapMarker

        exclude = ['partOfTrip', 'orderVisiting', 'confirmed', 'alreadyVisited']
        widgets = {'name' : forms.HiddenInput(),
                   'address' : forms.HiddenInput(),
                   'lat' : forms.HiddenInput(),
                   'lng' : forms.HiddenInput(),
                   'date' : forms.DateInput(),
                    }
        labels = { 'typeOfMarker' : 'Category'
            
            }

    

