# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('game', '0002_high_score'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cavern',
            name='title',
            field=models.TextField(default='', blank=True, db_index=True),
            preserve_default=True,
        ),
    ]
