from django import forms

from .models import UMusic


class UploadForm(forms.Form):
    file_field = forms.FileField(
        widget=forms.ClearableFileInput(attrs={'multiple': True})
        )


class UserMusicForm(forms.ModelForm):
    class Meta:
        model = UMusic
        fields = ['song_title']
        ## how to provide raised errors such as no blank song field