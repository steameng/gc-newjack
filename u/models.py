from django.db import models
from django.core.urlresolvers import reverse
from django.conf import settings



class UMusic(models.Model):
    '''Look at BaseUserManager to figure out password'''
    user = models.ForeignKey(settings.AUTH_USER_MODEL)
    creation_date = models.DateTimeField(auto_now_add=True, auto_now=False)  # only when created, never overwritten
    last_updated = models.DateTimeField(auto_now_add=False, auto_now=True)  # can be saved over
    song_title = models.CharField(verbose_name="Song Title", max_length=255, blank=False)


    def __unicode__(self):
        return  "{}".format(self.user)

    def get_absolute_url(self):
        return reverse("home", kwargs={"user": self.user})

