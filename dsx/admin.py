from django.contrib import admin

# Register your models here.
from .models import Person

class PersonAdmin(admin.ModelAdmin):
    list_display = ["__unicode__", "user_creation", "updated"]
    class Meta:
        model = Person

admin.site.register(Person, PersonAdmin)
