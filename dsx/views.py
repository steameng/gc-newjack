from django.shortcuts import render, redirect # Standard view rendering
from .forms import PersonForm, ContactForm, UploadForm # Pulling in form information
from django.views.generic import View # Standard View class
from django.contrib import messages # for success and other message
from django.core.mail import send_mail # to access send_mail function
from django.conf import settings # pulling email settings
from django.views.generic.edit import FormView
from random import randint
from scikits.audiolab import wavread, wavwrite
from scipy import vstack


# Create your views here.
class Home(View):
    '''This View collects member registration data and saves it in the Person's Model
        via the PersonForm ModelForm'''
    def get(self, request):
        form = ContactForm()
        context = {'form': form}
    #if request.user.is_authenticated(): # you can show different content based on auth
    #    context = {'user': request.user, 'email': request.user.email}
        return render(request, "dsx/home.html", context)

    def post(self, request):
        form = ContactForm(request.POST)
        if form.is_valid():
            #form_inst = form.save(commit=False)
            #do some customization to the fields here
            form.save()
            messages.success(request, "Registration Success!")
            return redirect("Home") #maybe put conditional if user is authenticated
        context = {'form': form}
        return render(request, "dsx/home.html", context)

class About(View):
    '''This View collects member registration data and saves it in the Person's Model
        via the PersonForm ModelForm'''
    def get(self, request):
        form = ContactForm()
        context = {'form': form}
    #if request.user.is_authenticated(): # you can show different content based on auth
    #    context = {'user': request.user, 'email': request.user.email}
        return render(request, "dsx/about.html", context)

    def post(self, request):
        form = ContactForm(request.POST)
        if form.is_valid():
            #form_inst = form.save(commit=False)
            #do some customization to the fields here
            form.save()
            messages.success(request, "Registration Success!")
            return redirect("About") #maybe put conditional if user is authenticated
        context = {'form': form}
        return render(request, "dsx/about.html", context)

class ContactPage(View):
    '''This View collects form data and also sends the user an email
        django email docs https://docs.djangoproject.com/en/1.10/topics/email/
        Might need to look at Captcha for sending a lot of emails
    '''
    def get(self, request):
        form = ContactForm()
        return render(request, "dsx/contact.html", {'form': form})

    def post(self, request):
        form = ContactForm(request.POST)
        if form.is_valid():
            form_data = form.cleaned_data
            message = form_data['message']
            subject = 'Site contact form'
            from_email = settings.EMAIL_HOST_USER
            to_email = [form_data['email']]
            # message=render_to_string(
            #     "chet/email/resolved_report.txt", {'report': form_submit, 'submitter': report.submitter}),
            # send_mail(
            #     subject,
            #     message,
            #     from_email,
            #     to_email,
            #     fail_silently=False
            # )

            messages.success(request, "Contact Form Submitted, check your email")
            return redirect("Home")
        return redirect("Contact")


class Upload(FormView):
    '''This View collects member registration data and saves it in the Person's Model
        via the PersonForm ModelForm'''
    form_class = UploadForm
    template_name = 'upload.html'  # Replace with your template.
    success_url = ''  # Replace with your URL or reverse().

    def get(self, request, *args, **kwargs):
        form = UploadForm()
        context = {'form': form}
    #if request.user.is_authenticated(): # you can show different content based on auth
    #    context = {'user': request.user, 'email': request.user.email}
        return render(request, "dsx/upload.html", context)

    def post(self, request, *args, **kwargs):
        file_name = []
        def handle_uploaded_files(f): ###USE STATIC TAG FOR MEDIA ROOT
            with open('/home/zato/Documents/sites/newjack/newjack/media/' + str(f), 'wb+') as destination:
                for chunk in f.chunks():
                    destination.write(chunk)
                file_name.append(str(f))
            return file_name

        form_class = self.get_form_class()
        form = self.get_form(form_class)
        files = request.FILES.getlist('file_field')
        if form.is_valid():
            for (i, f) in enumerate(files):
                file_name = handle_uploaded_files(f)

            #Put into function
            #Get arrays of files that match regex
            intros = filter(lambda x: 'intro' in x, file_name)
            verses = filter(lambda w: 'verse' in w, file_name)
            # outros = filter(lambda y: 'outro' in y, file_name)
            bridges = filter(lambda z: 'bridge' in z, file_name)
            fillers = filter(lambda u: 'filler' in u, file_name)

            #Choose random file from list
            intro = intros[randint(0, len(intros) - 1)]
            verse = verses[randint(0, len(verses) - 1)]
            bridge = bridges[randint(0, len(bridges) - 1)]
            # outro = outros[randint(0, len(outros) - 1)]
            filler = fillers[randint(0, len(fillers) - 1)]

            #Read the files
            intro_wav, fs, enc = wavread('/home/zato/Documents/sites/newjack/testfiles/newjack/wav/' + intro) #you will have to put file paths onto this
            bridge_wav, fs, enc = wavread('/home/zato/Documents/sites/newjack/testfiles/newjack/wav/' + bridge)
            verse_wav, fs, enc = wavread('/home/zato/Documents/sites/newjack/testfiles/newjack/wav/' + verse)
            # outro_wav, fs, enc = wavread(outro)
            filler_wav, fs, enc = wavread('/home/zato/Documents/sites/newjack/testfiles/newjack/wav/' + filler)

            #Stack the files into one file
            wave_file = vstack((intro_wav, verse_wav, filler_wav, bridge_wav))

            #Write the file to Media Dir
            wavwrite(wave_file, '/home/zato/Documents/sites/newjack/newjack/media/wave_file.wav', fs, enc) # will have to change absolute path for server

            #wave_file = intro + '_' + bridge + '_' + outro

            messages.success(request, "Passed, check files")
            context = {
                        'form': form,
                        'file_name': file_name,
                        'intro': intro,
                        'bridge': bridge,
                        'verse': verse,
                        'filler': filler,
                        # 'outro': outro,
                    }
            return render(request, "dsx/upload.html", context)
            #return redirect("Upload")
        else:
            return self.form_invalid(form)


class FeatureTwo(View):
    '''This View collects member registration data and saves it in the Person's Model
        via the PersonForm ModelForm'''
    def get(self, request):
        form = ContactForm()
        context = {'form': form}
    #if request.user.is_authenticated(): # you can show different content based on auth
    #    context = {'user': request.user, 'email': request.user.email}
        return render(request, "dsx/featuretwo.html", context)

    def post(self, request):
        form = ContactForm(request.POST)
        if form.is_valid():
            #form_inst = form.save(commit=False)
            #do some customization to the fields here
            form.save()
            messages.success(request, "Registration Success!")
            return redirect("FeatureTwo") #maybe put conditional if user is authenticated
        context = {'form': form}
        return render(request, "dsx/featuretwo.html", context)

class FeatureThree(View):
    '''This View collects member registration data and saves it in the Person's Model
        via the PersonForm ModelForm'''
    def get(self, request):
        form = ContactForm()
        context = {'form': form}
    #if request.user.is_authenticated(): # you can show different content based on auth
    #    context = {'user': request.user, 'email': request.user.email}
        return render(request, "dsx/featurethree.html", context)

    def post(self, request):
        form = ContactForm(request.POST)
        if form.is_valid():
            #form_inst = form.save(commit=False)
            #do some customization to the fields here
            form.save()
            messages.success(request, "Registration Success!")
            return redirect("FeatureThree") #maybe put conditional if user is authenticated
        context = {'form': form}
        return render(request, "dsx/featurethree.html", context)


class Pricing(View):
    '''This View collects member registration data and saves it in the Person's Model
        via the PersonForm ModelForm'''
    def get(self, request):
        form = ContactForm()
        context = {'form': form}
    #if request.user.is_authenticated(): # you can show different content based on auth
    #    context = {'user': request.user, 'email': request.user.email}
        return render(request, "dsx/pricing.html", context)

    def post(self, request):
        form = ContactForm(request.POST)
        if form.is_valid():
            #form_inst = form.save(commit=False)
            #do some customization to the fields here
            form.save()
            messages.success(request, "Registration Success!")
            return redirect("Pricing") #maybe put conditional if user is authenticated
        context = {'form': form}
        return render(request, "dsx/pricing.html", context)

class StyleGuide(View):
    '''This View collects member registration data and saves it in the Person's Model
        via the PersonForm ModelForm'''
    def get(self, request):
        return render(request, "dsx/styleguide.html")