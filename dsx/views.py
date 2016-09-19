from django.shortcuts import render, redirect # Standard view rendering
from .forms import PersonForm, ContactForm # Pulling in form information
from django.views.generic import View # Standard View class
from django.contrib import messages # for success and other message
from django.core.mail import send_mail # to access send_mail function
from django.conf import settings # pulling email settings


# Create your views here.
class HomePage(View):
    '''This View collects member registration data and saves it in the Person's Model
        via the PersonForm ModelForm'''
    def get(self, request):
        form = PersonForm()

    #if request.user.is_authenticated(): # you can show different content based on auth
    #    context = {'user': request.user, 'email': request.user.email}
        return render(request, "home.html", {'form': form})

    def post(self, request):
        form = PersonForm(request.POST)
        if form.is_valid():
            #form_inst = form.save(commit=False)
            #do some customization to the fields here
            form.save()

            messages.success(request, "Registration Success!")
            return redirect("HomePage") #maybe put conditional if user is authenticated

        return render(request, "home.html", {'form': form})

        #if form.is_valid():
            #instance = form.save(commit=False)
                #do some validation here

class ContactPage(View):
    '''This View collects form data and also sends the user an email
        django email docs https://docs.djangoproject.com/en/1.10/topics/email/
        Might need to look at Captcha for sending a lot of emails
    '''
    def get(self, request):
        form = ContactForm()
        return render(request, "contact.html", {'form': form})

    def post(self, request):
        form = ContactForm(request.POST)
        if form.is_valid():
            form_data = form.cleaned_data
            email = form_data['email']
            first_name = form_data['first_name']
            last_name = form_data['last_name']
            message = form_data['message']
            subject = 'Site contact form'

            from_email = settings.EMAIL_HOST_USER
            to_email = [from_email]
            send_mail(subject, message, from_email, to_email, fail_silently=False)

            messages.success(request, "Contact Form Submitted, check your email")
            context = {'form': form, 'form_data': form_data}
            #return redirect("/contact/", {'form': form, 'form_data': form_data}) # you can use this instead
            return render(request, "contact.html", context)
        return redirect("ContactPage")
