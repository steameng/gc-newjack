from django.shortcuts import render, redirect, get_object_or_404 # Standard view rendering
from django.views.generic import View # Standard View class
from django.contrib import messages # for success and other message
from django.core.mail import send_mail # to access send_mail function
from django.conf import settings # pulling email settings
from django.views.generic.edit import FormView, DeleteView, CreateView
from django.core.exceptions import PermissionDenied
from django.core.urlresolvers import reverse_lazy, reverse
from django.conf import settings
from django.http import HttpResponse

from .forms import  UploadForm, USongUploadForm , UMediaUploadForm, USongChoiceField, USongTitleForm
from .models import UMusic, UMedia
from .mizer import randomizer, randomizer_uploads

import json
import os
from os.path import basename


import wave


#from scikits.audiolab import wavread, wavwrite
#from scipy import vstack

#### Code for writing JSON to file
# import json
# with open('data.txt', 'w') as outfile:
#     json.dump(data, outfile)




class UHome(View):
    '''UserHomePage'''
    def get(self, request):
        if not request.user.is_authenticated():
            messages.info(request, "You have to Login")
            return redirect("Login")
        umediauploadform = UMediaUploadForm()
        usongtitleform = USongTitleForm
        songs = UMusic.objects.filter(user=request.user) # , umedia__id__in=[5,6]
        songfiles = UMedia.objects.filter(user=request.user)  # potentially turn this into a method
        testsong = songfiles[0]
        testjson = {'name': 'phil', 'number': 1234}



        context= {
            'umediauploadform': umediauploadform,
            'songs': songs,
            'songfiles': songfiles,
            'usongtitleform': usongtitleform,
            'testsong': testsong,
            'testjson': json.dumps(testjson),

            }
        return render(request, "u/home.html", context)

    def post(self, request):
        pass


class UHomeOld(View):
    '''UserHomePage'''
    def get(self, request):
        if not request.user.is_authenticated():
            messages.info(request, "You have to Login")
            return redirect("Login")
        # form = UserMusicForm()
        usongchoicefield = USongChoiceField()
        umediauploadform = UMediaUploadForm()
        usongtitleform = USongTitleForm
        # usonguploadform = USongUploadForm()
        songs = UMusic.objects.filter(user=request.user) # , umedia__id__in=[5,6]
        # print str(type(json.loads(songs[0].song_settings))) # type check for song_settings
        songfiles = UMedia.objects.filter(user=request.user)  # potentially turn this into a method
        song_created = False
        create = request.GET.get('usongfilechoiceform')
        a = request.GET
        if create:
            file_list = [v for k, v in a.items() if 'a__' in k]
            songfiles_list = UMedia.objects.filter(user=request.user, id__in=file_list)
            infiles = [
                (v.song_file.path, "{}".format(basename(os.path.splitext(v.song_file.path)[0])))
                for v in songfiles_list
                ]
            infiles = randomizer(infiles)
            print infiles
            data = []
            for (i, infile) in enumerate(infiles):
                # print infile[0]
                w = wave.open(infile[0], 'rb')
                data.append([w.getparams(), w.readframes(w.getnframes())])
                w.close()
            outfile = '/home/lupin/Documents/mannowar/newjack/newjack/media/wave_file.wav'
            output = wave.open(outfile, 'wb')
            output.setparams(data[0][0])
            for (i, infile) in enumerate(infiles):
                output.writeframes(data[i][1])
            output.close()
            messages.success(request, "Your song has been created")
            song_created = True

        context= {
            'umediauploadform': umediauploadform,
            'songs': songs,
            'songfiles': songfiles,
            'usongtitleform': usongtitleform,
            'song_created': song_created,
            }
        return render(request, "u/homeold.html", context)

    def post(self, request):
        songs = UMusic.objects.filter(user=request.user)  # potentially turn this into a method
        songfiles = UMedia.objects.filter(user=request.user)

        if not request.user.is_authenticated():
            messages.info(request, "You have to Login")
            return redirect("Login")

        if 'songfile' in request.POST:
            form = UMediaUploadForm(request.POST, request.FILES)
            if form.is_valid():

                files = request.FILES.getlist('file_field')
                for (i, song_file) in enumerate(files):
                    song_file = UMedia(song_file=song_file, user=request.user)
                    song_file.save()

                messages.success(request, 'File(s) Uploaded')
                return redirect("u:Home")

        elif 'newjack' in request.POST:
            a = request.POST
            fl1 = [{k: v} for k, v in a.items() if '1__' in k]
            fl2 = [{k: v} for k, v in a.items() if '2__' in k]
            fl3 = [{k: v} for k, v in a.items() if '3__' in k]
            fl4 = [{k: v} for k, v in a.items() if '4__' in k]
            file_list = fl1 + fl2 + fl3 + fl4
            if not file_list:
                messages.error(request, "you must put in some files")
                return redirect('u:HomeOld')
            jsonstring = json.dumps(file_list)
            song = UMusic(user=request.user, song_title=a['song_title'], song_settings=jsonstring)
            song.save()

            messages.success(request, "{}".format('settings saved'))
            return redirect('u:HomeOld')

        else:
            messages.error(request, 'error in submitting your form')
            return redirect("u:HomeOld")


class USong(View):
    '''USong Page'''

    def get(self, request, song_id):
        if not request.user.is_authenticated():
            messages.info(request, "You have to Login")
            return redirect("Login")
        umediauploadform = UMediaUploadForm()
        song = get_object_or_404(UMusic, user=request.user, id=song_id)
        song_json = json.loads(song.song_json)
        songfiles = UMedia.objects.filter(user=request.user)  # potentially turn this into a method

        # print song_json
        context= {
            'umediauploadform': umediauploadform,
            'song': song,
            'song_json': song_json,
            'songfiles': songfiles,
            }
        return render(request, "u/usong.html", context)

    def post(self, request):
        pass

class UploadSongFile(View):

    def post(self, request):
        form = UMediaUploadForm(request.POST, request.FILES)
        if form.is_valid():
            files = request.FILES.getlist('file_field')
            for (i, song_file) in enumerate(files):
                song_file = UMedia(song_file=song_file, user=request.user)
                song_file.save()

            messages.success(request, 'File(s) Uploaded')
            return redirect("u:Home")

class USongNew(View):
    '''USongNew Page'''

    def get(self, request):
        if not request.user.is_authenticated():
            messages.info(request, "You have to Login")
            return redirect("Login")
        umediauploadform = UMediaUploadForm()
        songfiles = UMedia.objects.filter(user=request.user)  # potentially turn this into a method

        context= {
            'umediauploadform': umediauploadform,
            'songfiles': songfiles,
            }
        return render(request, "u/usongnew.html", context)

    def post(self, request):
        pass

class SaveSong(View):
    def post(self, request):
        # print request.POST['savejson']
        # print json.dumps(request.POST['savejson'])
        song_title = request.POST['savesongtitle']
        song_json = json.dumps(request.POST['savejson'])
        #Update
        try:
            obj = UMusic.objects.get(song_title=song_title, user=request.user)
            obj.song_json = song_json
            obj.save()
        #Create if doesn't exist
        except UMusic.DoesNotExist:
            obj = UMusic(song_title=song_title, song_json=song_json, user=request.user)
            obj.save()
        # instance, created = UMusic.objects.update_or_create(song_title=song_title, user=request.user)
        # instance = UMusic(song_title=song_title, song_json=song_json, user=request.user)
        # instance.save()
        # print created
        messages.success(request, "Song Saved")
        # print json.loads(song_json)
        return redirect('u:USong', song_id=obj.id)


class DeleteSong(DeleteView):
    model = UMusic
    success_url = reverse_lazy("u:Home")


# class PlaySong(View):

    # def post(self, request):
    #     infiles = [
    #                 '/home/lupin/Documents/mannowar/newjack/newjack/media/user/mannowar/intro1.wav',
    #                 '/home/lupin/Documents/mannowar/newjack/newjack/media/user/mannowar/verse4.wav',
    #                 '/home/lupin/Documents/mannowar/newjack/newjack/media/user/mannowar/bridge3.wav'
    #                ]
    #     data = []
    #     for (i, infile) in enumerate(infiles):
    #         # print infile[0]
    #         w = wave.open(infile, 'rb')
    #         data.append([w.getparams(), w.readframes(w.getnframes())])
    #         w.close()
    #     outfile = '/home/lupin/Documents/mannowar/newjack/newjack/media/wave_file.wav'
    #     output = wave.open(outfile, 'wb')
    #     output.setparams(data[0][0])
    #     for (i, infile) in enumerate(infiles):
    #         output.writeframes(data[i][1])
    #     output.close()
    #     messages.success(request, "Your song has been created")
    #     return redirect("u:Home")
def playsong(request):
    infiles = [
        '/home/lupin/Documents/mannowar/newjack/newjack/media/user/mannowar/intro1.wav',
        '/home/lupin/Documents/mannowar/newjack/newjack/media/user/mannowar/verse4.wav',
        '/home/lupin/Documents/mannowar/newjack/newjack/media/user/mannowar/bridge3.wav'
    ]
    data = []
    for (i, infile) in enumerate(infiles):
        # print infile[0]
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
    messages.success(request, "Your song has been created")
    return HttpResponse(songdata, content_type='audio/wav')

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
            infiles = randomizer_uploads(form_files)
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





class USongold(View):
    '''USong Page'''

    def get(self, request, song_id):
        if not request.user.is_authenticated():
            messages.info(request, "You have to Login")
            return redirect("Login")
        usonguploadform = USongUploadForm()
        song = get_object_or_404(UMusic, user=request.user, id=song_id)
        # data = UMusic.objects.get(user=request.user, id=song_id) # get_object_or_404
        songfiles = UMedia.objects.filter(user=request.user,
                                          song=song)  # potentially turn this into a method
        context = {
            # 'form': form,
            # 'umediaform': umediaform,
            'song': song,
            'songfiles': songfiles,
            'usonguploadform': usonguploadform,
        }
        return render(request, "u/usong.html", context)





#
# class UHome(View):
#     '''UserHomePage'''
#     def get(self, request):
#         if not request.user.is_authenticated():
#             messages.info(request, "You have to Login")
#             return redirect("Login")
#         # form = UserMusicForm()
#         usongchoicefield = USongChoiceField()
#         umediauploadform = UMediaUploadForm()
#         usongtitleform = USongTitleForm
#         # usonguploadform = USongUploadForm()
#         songs = UMusic.objects.filter(user=request.user) # , umedia__id__in=[5,6]
#         # print str(type(json.loads(songs[0].song_settings))) # type check for song_settings
#         songfiles = UMedia.objects.filter(user=request.user)  # potentially turn this into a method
#         song_created = False
#         create = request.GET.get('usongfilechoiceform')
#         a = request.GET
#         if create:
#             file_list = [v for k, v in a.items() if 'a__' in k]
#             # print file_list
#             songfiles_list = UMedia.objects.filter(user=request.user, id__in=file_list)
#             # print songfiles_list
#             # form_files = []
#             # for (i, f) in enumerate(songfiles_list):
#             #     # form_files = handle_uploaded_files(f)
#             #     form_files.append(f.song_file)
#
#             # print form_files[0].path
#             # path = "/media/{}".format(form_files[0].name)
#             # file = open(form_files[0].path, "r")
#             # print file.read()
#             # print settings.MEDIA_ROOT
#             # print songfiles_list
#             # print songfiles_list[0].song_file.name
#             infiles = [
#                 (v.song_file.path, "{}".format(basename(os.path.splitext(v.song_file.path)[0])))
#                 for v in songfiles_list
#                 ]
#             # print infiles
#             # file_label_list = ["{}".format(basename(os.path.splitext(v)[0])) for v in infiles]
#             # print file_label_list
#
#             # print infiles
#
#             # print ['something', None, 'somethingelse']
#             #
#             # tests = filter(lambda x: 'test' in x[1], infiles)
#             # fillers = filter(lambda x: 'filler' in x[1], infiles)
#             # verses = filter(lambda x: 'verse' in x[1], infiles)
#
#             # test = ''
#             # verse = ''
#             # filler = ''
#             # test = tests[randint(0, len(tests) - 1)]
#             # if verses:
#             #     verse = test[randint(0, len(verse) - 1)]
#             # if fillers:
#             #     filler = fillers[randint(0, len(fillers) - 1)]
#             # print filter(None, [test, filler, verse])
#
#             # intro = test[randint(0, len(test) - 1)]
#             # print intro
#             ### Variation of above
#             # test = [v for i, v in enumerate(infiles) if 'test' in v[1]]
#             # print test
#
#             infiles = randomizer(infiles)
#             print infiles
#             data = []
#             for (i, infile) in enumerate(infiles):
#                 print infile[0]
#                 w = wave.open(infile[0], 'rb')
#                 data.append([w.getparams(), w.readframes(w.getnframes())])
#                 w.close()
#
#             outfile = '/home/lupin/Documents/mannowar/newjack/newjack/media/wave_file.wav'
#             output = wave.open(outfile, 'wb')
#             output.setparams(data[0][0])
#             for (i, infile) in enumerate(infiles):
#                 output.writeframes(data[i][1])
#             output.close()
#             messages.success(request, "Your song has been created")
#             song_created = True
#
#
#         context= {
#             # 'form': form,
#             'umediauploadform': umediauploadform,
#             'songs': songs,
#             'songfiles': songfiles,
#             'usongtitleform': usongtitleform,
#             # 'usonguploadform': usonguploadform,
#             # 'usongchoicefield': usongchoicefield,
#             'song_created': song_created,
#             }
#         return render(request, "u/home.html", context)
#
#     def post(self, request):
#         songs = UMusic.objects.filter(user=request.user)  # potentially turn this into a method
#         songfiles = UMedia.objects.filter(user=request.user)
#
#         if not request.user.is_authenticated():
#             messages.info(request, "You have to Login")
#             return redirect("Login")
#
#         # if 'songtitle' in request.POST:
#         #     form = UserMusicForm(request.POST)
#         #     if form.is_valid():
#         #         instance = form.save(commit=False)
#         #         instance.user = request.user
#         #         instance.save()
#         #
#         #         messages.success(request, "Song Submitted")
#         #         return redirect("u:Home")
#         if 'songfile' in request.POST:
#             form = UMediaUploadForm(request.POST, request.FILES)
#             if form.is_valid():
#
#                 files = request.FILES.getlist('file_field')
#                 for (i, song_file) in enumerate(files):
#                     song_file = UMedia(song_file=song_file, user=request.user)
#                     song_file.save()
#
#                 messages.success(request, 'File(s) Uploaded')
#                 return redirect("u:Home")
#
#                 # instance = form.save(commit=False)
#                 # instance.user = request.user
#                 # instance.save()
#                 #
#                 # messages.success(request, "SongFile Submitted")
#                 # return redirect("u:Home")
#         elif 'newjack' in request.POST:
#             # print request.POST
#             a = request.POST
#             # checklist = ['1__','2__','3__','4__']
#             fl1 = [{k: v} for k, v in a.items() if '1__' in k]
#             fl2 = [{k: v} for k, v in a.items() if '2__' in k]
#             fl3 = [{k: v} for k, v in a.items() if '3__' in k]
#             fl4 = [{k: v} for k, v in a.items() if '4__' in k]
#             file_list = fl1 + fl2 + fl3 + fl4
#             if not file_list:
#                 messages.error(request, "you must put in some files")
#                 return redirect('u:Home')
#             jsonstring = json.dumps(file_list)
#             print jsonstring
#             jsonobj = json.loads(jsonstring)
#
#             # form = USongTitleForm(request.POST)
#             # if form.is_valid():
#             #     data = form.cleaned_data
#             song = UMusic(user=request.user, song_title=a['song_title'], song_settings=jsonstring)
#             song.save()
#
#             messages.success(request, "{}".format('settings saved'))
#             return redirect('u:Home')
#         elif 'songupload' in request.POST:
#             form = USongUploadForm(request.POST, request.FILES)
#
#             if form.is_valid():
#
#                 data = form.cleaned_data
#                 song_title = UMusic(song_title=data['song_title'], user=request.user)
#                 song_title.save()
#
#                 files = request.FILES.getlist('file_field')
#                 for (i, song_file) in enumerate(files):
#                     song_file = UMedia(song_file=song_file, user=request.user)
#                     song_file.save()
#                     song_file.song.add(song_title) # associating to manytomany
#
#                 messages.success(request, '{} uploaded'.format(song_title.song_title))
#                 return redirect("u:Home")
#             return render(request, "u/home.html", {'usonguploadform': form, 'songs': songs, 'songfiles': songfiles})
#         elif 'usongfilechoiceform' in request.POST:
#             print request.POST
#             messages.success(request, "success post")
#             return redirect("u:Home")
#         else:
#             messages.error(request, 'error in submitting your form')
#             return redirect("u:Home")
#
#         #
#         # messages.error(request, 'something happened')
#         # return redirect("u:Home")