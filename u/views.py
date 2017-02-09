from django.shortcuts import render, redirect # Standard view rendering
from django.views.generic import View # Standard View class
from django.contrib import messages # for success and other message
from django.core.mail import send_mail # to access send_mail function
from django.conf import settings # pulling email settings
from django.views.generic.edit import FormView, DeleteView
from django.core.exceptions import PermissionDenied
from django.core.urlresolvers import reverse_lazy


from .forms import  UploadForm, UserMusicForm
from .models import UMusic

from random import randint
import wave
#from scikits.audiolab import wavread, wavwrite
#from scipy import vstack



class UserHomePage(View):
    '''UserHomePage'''
    def get(self, request):
        if not request.user.is_authenticated():
            messages.info(request, "You have to Login")
            return redirect("Login")
        form = UserMusicForm()
        data = UMusic.objects.filter(user=request.user) # potentially turn this into a method
        context= {
            'form': form,
            'data': data,
            }
        return render(request, "u/home.html", context)

    def post(self, request):
        if not request.user.is_authenticated():
            messages.info(request, "You have to Login")
            return redirect("Login")
        form = UserMusicForm(request.POST)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.user = request.user
            instance.save()

            messages.success(request, "Song Submitted")
            return redirect("u:Home")
        messages.error(request, "Looks like something went wrong")
        return redirect("u:Home")



class DeleteSong(DeleteView):
    model = UMusic
    success_url = reverse_lazy("u:Home")
