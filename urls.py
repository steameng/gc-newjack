"""ds_site URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.8/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add an import:  from blog import urls as blog_urls
    2. Add a URL to urlpatterns:  url(r'^blog/', include(blog_urls))
"""
from django.conf.urls import include, url
from django.contrib import admin
#from django.contrib.auth.decorators import login_required
from django.conf.urls.static import static # if error this might be it
from django.conf import settings
import stage.urls
import dsx.views
import views


urlpatterns = [
    url(r'^admin/', include(admin.site.urls), name="admin"), # admin urls
    url(r'^accounts/', include('registration.backends.default.urls')), # registration urls
    url(r'^$', dsx.views.Home.as_view(), name='Home'),
    url(r'^about/$', dsx.views.About.as_view(), name='About'),
    url(r'^contact/$', dsx.views.ContactPage.as_view(), name='Contact'),
    url(r'^upload/$', dsx.views.Upload.as_view(), name='Upload'),
    url(r'^featuretwo/$', dsx.views.FeatureTwo.as_view(), name='FeatureTwo'),
    url(r'^featurethree/$', dsx.views.FeatureThree.as_view(), name='FeatureThree'),
    url(r'^pricing/$', dsx.views.Pricing.as_view(), name='Pricing'),
    url(r'^styleguide/$', dsx.views.StyleGuide.as_view(), name='StyleGuide'),


    url(r'^stage/', include(stage.urls, 'stage', 'stage')), # stage pages


    # url(r'^bs_theme/$', dsx.views.BSTheme.as_view(), name='BSTheme'),
    # url(r'^mat_starter/$', dsx.views.MatStarter.as_view(), name='MatStarter'),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
