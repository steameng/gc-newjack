# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('u', '0002_umusic_song_settings'),
    ]

    operations = [
        migrations.RenameField(
            model_name='umusic',
            old_name='song_settings',
            new_name='song_json',
        ),
    ]
