# from django.core.mail import send_mail # to access send_mail function
# from django.core.exceptions import PermissionDenied
# from django.conf import settings

# from os.path import basename
# from scikits.audiolab import wavread, wavwrite
# from scipy import vstack
from django.shortcuts import render, redirect, get_object_or_404 # Standard view rendering
from django.views.generic import View # Standard View class
from django.contrib import messages # for success and other message
from django.http import HttpResponse
from django.core.urlresolvers import reverse_lazy, reverse
from django.views.generic.edit import FormView, DeleteView, CreateView
from django.conf import settings

from .forms import UMediaUploadForm
from .models import UMusic, UMedia

import json
import wave
from algorythm import getwavs

import logging
# import os
import cloudstorage as gcs
# import webapp2
# from google.appengine.api import app_identity

##GCS Storage bucket info
bucket_name = 'newjack-steameng.appspot.com'
bucket = '/' + bucket_name

##############################  VIEWS  #################################

class DeleteSong(View):
    def post(self, request, song_id):
        song = get_object_or_404(UMusic, user=request.user, id=song_id )
        song_title = song.song_title
        song.delete()

        messages.success(request, "Song: {} Deleted".format(song_title))
        return redirect('u:Home')

    def get(self, request, song_id):
        song = get_object_or_404(UMusic, user=request.user, id=song_id)
        context = {
            'song': song,
        }
        return render(request, 'u/song_confirm_delete.html', context)

class DeleteSongOld(DeleteView):
    model = UMusic
    success_url = reverse_lazy("u:Home")


def playsong(request, song_id, song_seed):
    '''Grabs current song to get json.
     Gets seed from last page seed value and magic'''
    file_path = '/newjack-steameng.appspot.com/pmanno/intro1.wav'
    gcs_file = gcs.open(file_path)
    song_data = gcs_file.read()
    gcs_file.close()

    return HttpResponse(song_data, content_type='audio/wav')
    # song = get_object_or_404(UMusic, user=request.user, id=song_id)
    # song_json = json.loads(song.song_json)
    #
    # infiles = getwavs(song_json, song_seed) # get paths from algorythm
    #
    #

    # data = []
    # for (i, infile) in enumerate(infiles):
    #     #must read gcs_file here
    #     w = wave.open(infile, 'rb')
    #     data.append([w.getparams(), w.readframes(w.getnframes())])
    #     w.close()

    #
    # outfile = settings.MEDIA_ROOT + '/user/{}'.format(request.user) +'/wave_file.wav'
    # output = wave.open(outfile, 'wb')
    # output.setparams(data[0][0])
    # for (i, infile) in enumerate(infiles):
    #     output.writeframes(data[i][1])
    # output.close()
    #
    # with open(outfile, 'r') as fp:
    #     songdata = fp.read()
    #       fp.close() #### ADDED THIS LINE, STILL NEED TO TEST
    #
    # return HttpResponse(songdata, content_type='audio/wav')


class UHome(View):
    '''UserHomePage'''
    def get(self, request):
        if not request.user.is_authenticated():
            messages.info(request, "You have to Login")
            return redirect("Login")

        umediauploadform = UMediaUploadForm()
        songs = UMusic.objects.filter(user=request.user)
        songfiles = UMedia.objects.filter(user=request.user)

        context= {
            'umediauploadform': umediauploadform,
            'songs': songs,
            'songfiles': songfiles,
            }
        return render(request, "u/home.html", context)



class USong(View):
    '''Gets the requested Song Page'''

    def get(self, request, song_id):
        if not request.user.is_authenticated():
            messages.info(request, "You have to Login")
            return redirect("Login")
        umediauploadform = UMediaUploadForm()
        song = get_object_or_404(UMusic, user=request.user, id=song_id)
        song_json = song.song_json
        songfiles = UMedia.objects.filter(user=request.user)

        context= {
            'umediauploadform': umediauploadform,
            'song': song,
            'song_json': song_json,
            'songfiles': songfiles,
            }
        return render(request, "u/usong.html", context)



class USongNew(View):
    '''Creates a Blank Template '''

    def get(self, request):
        if not request.user.is_authenticated():
            messages.info(request, "You have to Login")
            return redirect("Login")
        umediauploadform = UMediaUploadForm()
        songfiles = UMedia.objects.filter(user=request.user)

        context= {
            'umediauploadform': umediauploadform,
            'songfiles': songfiles,
            }
        return render(request, "u/usongnew.html", context)



class SaveSong(View):
    '''Saves Song and either Creates or Updates song in DB'''

    def post(self, request):
        song_title = request.POST['savesongtitle']
        song_json = request.POST['savejson']
        song_seed = request.POST['saveseed']
        # Update
        try:
            instance = UMusic.objects.get(song_title=song_title, user=request.user)
            instance.song_json = song_json
            instance.song_seed = song_seed
            instance.save()

            messages.success(request, "Song Updated")
        # Create if doesn't exist
        except UMusic.DoesNotExist:
            instance = UMusic(song_title=song_title, song_json=song_json, song_seed=song_seed, user=request.user)
            instance.save()

            messages.success(request, "Song Saved")
        return redirect('u:USong', song_id=instance.id)



class UploadSongFile(View):
    '''Multi-file Upload Handler'''

    def post(self, request):
        form = UMediaUploadForm(request.POST, request.FILES)
        if form.is_valid():
            files = request.FILES.getlist('file_field')
            for (i, song_file) in enumerate(files):
                data = []
                write_retry_params = gcs.RetryParams(backoff_factor=1.1)
                song_name = str(request.user) + '/' + song_file.name
                file_path = bucket + '/' + song_name



                # w = wave.open(song_file, 'rb')
                # data.append([w.getparams(), w.readframes(w.getnframes())])
                # w.close()
                #
                # output = wave.open(song_file, 'wb')
                # output.setparams(data[0][0])
                # output.writeframes(data[i][1])
                # output.close()

                with open(song_file.file, 'rb') as fp:
                    obj = fp.read()
                gcs_file = gcs.open(file_path, 'w', content_type='audio/x-wav', retry_params=write_retry_params)
                gcs_file.write(obj)
                gcs_file.close()




                song_file = UMedia(song_file=song_name, user=request.user)
                song_file.save()

            return redirect("u:Home")
