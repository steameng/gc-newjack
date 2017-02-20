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
from django.conf.urls import include, url, patterns
from django.contrib import admin
#from django.contrib.auth.decorators import login_required
from django.conf.urls.static import static # if error this might be it
from django.conf import settings

import views



urlpatterns = [

    url(r'^$', views.UHome.as_view(), name='Home'),
    url(r'^old/$', views.UHomeOld.as_view(), name='HomeOld'),
    url(r'^upload/$', views.Upload.as_view(), name='Upload'),
    url(r'^song/(?P<song_id>\d+)/$', views.USong.as_view(), name='Song'),
    url(r'^(?P<pk>\d+)/delete/$', views.DeleteSong.as_view(), name='DeleteSong'),

]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


if not settings.DEBUG:
    urlpatterns += patterns('',
        (r'^static/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.STATIC_ROOT}),
    )