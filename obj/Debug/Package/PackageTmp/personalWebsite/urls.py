"""
Definition of urls for personalWebsite.
"""

from datetime import datetime
from django.conf.urls import url, include
import django.contrib.auth.views
from django.conf import settings
from django.conf.urls.static import static

import app.forms
import app.views

# Uncomment the next lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = [
    # Examples:
    url(r'^$', app.views.home, name='home'),
    url(r'^contact$', app.views.contact, name='contact'),
    url(r'^about', app.views.about, name='about'),
    url(r'^tripoutline', app.views.tripoutline, name='tripoutline'),
    url(r'^login/$',
        django.contrib.auth.views.login,
        {
            'template_name': 'app/login.html',
            'authentication_form': app.forms.BootstrapAuthenticationForm,
            'extra_context':
            {
                'title': 'Log in',
                'year': datetime.now().year,
            }
        },
        name='login'),
    url(r'^logout$',
        django.contrib.auth.views.logout,
        {
            'next_page': '/',
        },
        name='logout'),
    url(r'^bythenumbers/', app.views.bythenumbers, name='bythenumbers'),
    url(r'^signup', app.views.signup, name='signup'),
    url(r'^photos', app.views.photos, name='photos'),
    url(r'^blogs/(?P<slug>[^\.]+)',
        app.views.view_blog_post,
        name='view_blog_post'),
    url(
        r'^category/(?P<slug>[^\.]+).html',
        app.views.view_category,
        name='view_blog_category'
        ),
    url(r'^album/(?P<slug>[^\.]+).html',
        app.views.view_album,
        name='view_album'
        ),
        
    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
     url(r'^admin/', include(admin.site.urls)),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
