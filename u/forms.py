from django import forms
from django.contrib.auth.models import User
from .models import UMusic, UMedia


# class UserForm(forms.ModelForm):
#     password = forms.CharField(widget=forms.PasswordInput)
#
#     class Meta:
#         model = User
#         field = ['username','email','password']




# class UserMusicForm(forms.ModelForm):
#     class Meta:
#         model = UMusic
#         fields = ['song_title']
#         ## how to provide raised errors such as no blank song field
#
#

# class UMediaForm(forms.ModelForm):
#     class Meta:
#         model = UMedia
#         fields = ['song_file']

class UMediaUploadForm(forms.Form):
    file_field = forms.FileField(required=True, widget=forms.ClearableFileInput(attrs={'multiple': True}))





class USongUploadForm(forms.Form):
    file_field = forms.FileField(required=False, widget=forms.ClearableFileInput(attrs={'multiple': True}))
    song_title = forms.CharField(required=False, max_length=255)

    def clean_song_title(self):
        song_title = self.cleaned_data.get('song_title')
        if not song_title:
            raise forms.ValidationError("Song title required")
        return song_title




class UploadForm(forms.Form):
    file_field = forms.FileField(widget=forms.ClearableFileInput(attrs={'multiple': True})
        )

class USongChoiceField(forms.Form):
    file_field = forms.ModelMultipleChoiceField(
        queryset=UMedia.objects.filter(user=1),
        widget=forms.CheckboxSelectMultiple()
    )