# from django.core.mail import send_mail # to access send_mail function
# from django.core.exceptions import PermissionDenied
# from django.conf import settings
# import os
# from os.path import basename
# from scikits.audiolab import wavread, wavwrite
# from scipy import vstack
from django.shortcuts import render, redirect, get_object_or_404 # Standard view rendering
from django.views.generic import View # Standard View class
from django.contrib import messages # for success and other message
from django.http import HttpResponse
from django.core.urlresolvers import reverse_lazy, reverse
from django.views.generic.edit import FormView, DeleteView, CreateView

from .forms import UMediaUploadForm
from .models import UMusic, UMedia

import json
import wave
from algorythm import getwavs



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

    song = get_object_or_404(UMusic, user=request.user, id=song_id)
    song_json = json.loads(json.loads(song.song_json))

    infiles = getwavs(song_json, song_seed) # get paths from algorythm

    data = []
    for (i, infile) in enumerate(infiles):
        w = wave.open(infile, 'rb')
        data.append([w.getparams(), w.readframes(w.getnframes())])
        w.close()

    outfile = '/home/lupin/Documents/mannowar/newjack/newjack/media/wave_file.wav'
    output = wave.open(outfile, 'wb')
    output.setparams(data[0][0])
    for (i, infile) in enumerate(infiles):
        output.writeframes(data[i][1])
    output.close()

    with open(outfile, 'r') as fp:
        songdata = fp.read()

    return HttpResponse(songdata, content_type='audio/wav')


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
        song_json = json.loads(song.song_json)
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
        song_json = json.dumps(request.POST['savejson'])
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
                song_file = UMedia(song_file=song_file, user=request.user)
                song_file.save()

            messages.success(request, 'File(s) Uploaded')
            return redirect("u:Home")
