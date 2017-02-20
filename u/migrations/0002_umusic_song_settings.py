# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import datetime
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('u', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='umusic',
            name='song_settings',
            field=models.TextField(default=datetime.datetime(2017, 2, 19, 2, 28, 44, 989356, tzinfo=utc)),
            preserve_default=False,
        ),
    ]
