from django.shortcuts import render, redirect # Standard view rendering

from django.views.generic import View # Standard View class
from django.contrib import messages # for success and other message
from django.core.mail import send_mail # to access send_mail function
from django.conf import settings # pulling email settings


# Create your views here.


class BSTheme(View):
    '''BS Theme template view'''
    def get(self, request):
        return render(request, "stage/bs_theme.html")

    def post(self, request):
        return render(request, "stage/bs_theme.html")

class MatStarter(View):
    '''BS Theme template view'''
    def get(self, request):
        return render(request, "stage/mat_starter.html")

    def post(self, request):
        return render(request, "stage/mat_starter.html")


class Base(View):
    '''Base template view'''
    def get(self, request):
        return render(request, "stage/base.html")

    def post(self, request):
        return render(request, "stage/base.html")

class HomeStage(View):
    '''Base template view'''
    def get(self, request):
        return render(request, "stage/homestage.html")

    def post(self, request):
        return render(request, "stage/homestage.html")

