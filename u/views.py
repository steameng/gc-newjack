from django.shortcuts import render, redirect, get_object_or_404 # Standard view rendering
from django.views.generic import View # Standard View class
from django.contrib import messages # for success and other message
from django.core.mail import send_mail # to access send_mail function
from django.conf import settings # pulling email settings
from django.views.generic.edit import FormView, DeleteView
from django.core.exceptions import PermissionDenied
from django.core.urlresolvers import reverse_lazy


from .forms import  UploadForm, USongUploadForm , UMediaUploadForm, USongChoiceField # UserMusicForm,
from .models import UMusic, UMedia

from random import randint
import wave
from .mizer import randomizer

#from scikits.audiolab import wavread, wavwrite
#from scipy import vstack



class UHome(View):
    '''UserHomePage'''
    def get(self, request):
        if not request.user.is_authenticated():
            messages.info(request, "You have to Login")
            return redirect("Login")
        # form = UserMusicForm()
        usongchoicefield = USongChoiceField()
        umediauploadform = UMediaUploadForm()
        usonguploadform = USongUploadForm()
        songs = UMusic.objects.filter(user=request.user) # , umedia__id__in=[5,6]
        songfiles = UMedia.objects.filter(user=request.user)  # potentially turn this into a method

        create = request.GET.get('usongfilechoiceform')
        a = request.GET
        print a




        context= {
            # 'form': form,
            'umediauploadform': umediauploadform,
            'songs': songs,
            'songfiles': songfiles,
            'usonguploadform': usonguploadform,
            'usongchoicefield': usongchoicefield,
            }
        return render(request, "u/home.html", context)

    def post(self, request):
        songs = UMusic.objects.filter(user=request.user)  # potentially turn this into a method
        songfiles = UMedia.objects.filter(user=request.user)

        if not request.user.is_authenticated():
            messages.info(request, "You have to Login")
            return redirect("Login")

        # if 'songtitle' in request.POST:
        #     form = UserMusicForm(request.POST)
        #     if form.is_valid():
        #         instance = form.save(commit=False)
        #         instance.user = request.user
        #         instance.save()
        #
        #         messages.success(request, "Song Submitted")
        #         return redirect("u:Home")
        if 'songfile' in request.POST:
            form = UMediaUploadForm(request.POST, request.FILES)
            if form.is_valid():
                if form.is_valid():

                    files = request.FILES.getlist('file_field')
                    for (i, song_file) in enumerate(files):
                        song_file = UMedia(song_file=song_file, user=request.user)
                        song_file.save()

                    messages.success(request, 'File(s) Uploaded')
                    return redirect("u:Home")

                # instance = form.save(commit=False)
                # instance.user = request.user
                # instance.save()
                #
                # messages.success(request, "SongFile Submitted")
                # return redirect("u:Home")
        elif 'songupload' in request.POST:
            form = USongUploadForm(request.POST, request.FILES)

            if form.is_valid():

                data = form.cleaned_data
                song_title = UMusic(song_title=data['song_title'], user=request.user)
                song_title.save()

                files = request.FILES.getlist('file_field')
                for (i, song_file) in enumerate(files):
                    song_file = UMedia(song_file=song_file, user=request.user)
                    song_file.save()
                    song_file.song.add(song_title)

                messages.success(request, '{} uploaded'.format(song_title.song_title))
                return redirect("u:Home")
            return render(request, "u/home.html", {'usonguploadform': form, 'songs': songs, 'songfiles': songfiles})
        elif 'usongfilechoiceform' in request.POST:
            print request.POST
            messages.success(request, "success post")
            return redirect("u:Home")
        else:
            messages.error(request, 'error in submitting your form')
            return redirect("u:Home")

        #
        # messages.error(request, 'something happened')
        # return redirect("u:Home")


class USong(View):
    '''USong Page'''
    def get(self, request, song_id):
        if not request.user.is_authenticated():
            messages.info(request, "You have to Login")
            return redirect("Login")
        usonguploadform = USongUploadForm()
        song = get_object_or_404(UMusic, user=request.user, id=song_id)
        # data = UMusic.objects.get(user=request.user, id=song_id) # get_object_or_404
        songfiles = UMedia.objects.filter(user=request.user, song=song)  # potentially turn this into a method
        context= {
            # 'form': form,
            # 'umediaform': umediaform,
            'song': song,
            'songfiles': songfiles,
            'usonguploadform': usonguploadform,
            }
        return render(request, "u/song.html", context)



class DeleteSong(DeleteView):
    model = UMusic
    success_url = reverse_lazy("u:Home")



class Upload(FormView):

    form_class = UploadForm
    template_name = 'upload.html'  # Replace with your template.
    success_url = ''  # Replace with your URL or reverse().

    def get(self, request, *args, **kwargs):
        form = UploadForm()
        context = {'form': form}
        # if request.user.is_authenticated(): # you can show different content based on auth
        #    context = {'user': request.user, 'email': request.user.email}
        return render(request, "u/upload.html", context)

    def post(self, request, *args, **kwargs):


        # def handle_uploaded_files(f):  ###USE STATIC TAG FOR MEDIA ROOT
        #     with open('/home/lupin/Documents/mannowar/newjack/newjack/media/' + str(f), 'wb+') as destination:
        #         for chunk in f.chunks():
        #             destination.write(chunk)
        #         form_files.append(str(f))
        #     return form_files
        form_files = []
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        files = request.FILES.getlist('file_field')
        if form.is_valid():
            for (i, f) in enumerate(files):
                # form_files = handle_uploaded_files(f)
                form_files.append(f)

            ### Contstruct Output
            infiles = randomizer(form_files)
            #### WRITE FILES DEF

            data = []
            for infile in infiles:
                w = wave.open(infile, 'rb')
                data.append([w.getparams(), w.readframes(w.getnframes())])
                w.close()

            outfile = '/home/lupin/Documents/mannowar/newjack/newjack/media/wave_file.wav'
            output = wave.open(outfile, 'wb')
            output.setparams(data[0][0])
            for (i, infile) in enumerate(infiles):
                output.writeframes(data[i][1])
            output.close()

            messages.success(request, "Passed, check files")
            context = {
                'form': form,
                'files': form_files,
                # 'intro': intro,
                # 'bridge': bridge,
                # 'verse': verse,
                # 'filler': filler,
                # 'outro': outro,
            }
            return render(request, "u/upload.html", context)
            # return redirect("Upload")
        else:
            return self.form_invalid(form)
