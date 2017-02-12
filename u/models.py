from django.db import models
from django.core.urlresolvers import reverse
from django.conf import settings
from django.db.models.signals import pre_save
from django.utils.text import slugify
import os
from os.path import basename

def user_directory_path(instance, filename):
    # file will be uploaded to MEDIA_ROOT/user_<id>/<filename>
    return 'user/{0}/{1}'.format(instance.user, filename)



class UPerson(models.Model):
    '''Look at BaseUserManager to figure out password'''
    user = models.ForeignKey(settings.AUTH_USER_MODEL)
    creation_date = models.DateTimeField(auto_now_add=True, auto_now=False)  # only when created, never overwritten
    info = models.CharField(verbose_name="Song Title", max_length=255, blank=False)

    def __unicode__(self):
        return  "{}".format(self.user)



class UMusic(models.Model):
    '''Look at BaseUserManager to figure out password'''
    user = models.ForeignKey(settings.AUTH_USER_MODEL)
    creation_date = models.DateTimeField(auto_now_add=True, auto_now=False)  # only when created, never overwritten
    last_updated = models.DateTimeField(auto_now_add=False, auto_now=True)  # can be saved over
    song_title = models.CharField(verbose_name="Song Title", max_length=255, blank=False)


    def __unicode__(self):
        return "{}".format(self.user)

    def get_absolute_url(self):
        return reverse("u:Song", kwargs={"song_id": self.id})



class UMedia(models.Model):
    '''Contains User Song Files, each file is related to a song'''
    user = models.ForeignKey(settings.AUTH_USER_MODEL)
    song = models.ManyToManyField(UMusic)
    creation_date = models.DateTimeField(auto_now_add=True, auto_now=False)  # only when created, never overwritten
    song_file = models.FileField(upload_to=user_directory_path)


    def __unicode__(self):
        return "{}".format(self.user)


    def label(self):
        return "{}".format(basename(os.path.splitext(self.song_file.name)[0]))



# def pre_save_post_signal_receiver(sender, instance, *args, **kwargs):
#     slug = slugify("{}".format(basename(os.path.splitext(instance.song_file.name)[0])))
#     exists = UMedia.objects.filter(slug=slug).exists()
#     if exists:
#         slug = "{0}-{1}".format(slug, instance.id)
#     instance.slug = slug
#
# pre_save.connect(pre_save_post_signal_receiver, sender=UMedia)
