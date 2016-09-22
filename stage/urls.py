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

import views

urlpatterns = [
    # url(r'^$', dsx.views.HomePage.as_view(), name='HomePage'),
    # url(r'^contact/$', dsx.views.ContactPage.as_view(), name='ContactPage'),
    url(r'^bs_theme/$', views.BSTheme.as_view(), name='BSTheme'),
    url(r'^mat_starter/$', views.MatStarter.as_view(), name='MatStarter'),
    url(r'^base/$', views.Base.as_view(), name='Base'),
    url(r'^homestage/$', views.HomeStage.as_view(), name='HomeStage'),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
