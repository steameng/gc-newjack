from django.contrib import admin

# Register your models here.
from .models import Person, UserMusic
from .forms import PersonForm, UserMusicForm

class PersonAdmin(admin.ModelAdmin):
    list_display = ["__unicode__", "creation_date", "last_updated"]
    form = PersonForm
    #class Meta:
    #   model = Person

class UserMusicAdmin(admin.ModelAdmin):
    list_display = ["__unicode__", "creation_date", "last_updated"]
    form = UserMusicForm
    #class Meta:
    #   model = Person

admin.site.register(Person, PersonAdmin)
admin.site.register(UserMusic, UserMusicAdmin)
