from django.contrib import admin

# Register your models here.
from .models import Person
from .forms import PersonForm

class PersonAdmin(admin.ModelAdmin):
    list_display = ["__unicode__", "user_creation", "updated"]
    form = PersonForm
    #class Meta:
    #   model = Person

admin.site.register(Person, PersonAdmin)
