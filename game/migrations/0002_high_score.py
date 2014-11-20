# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('game', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='High_Score',
            fields=[
                ('id', models.AutoField(primary_key=True, verbose_name='ID', serialize=False, auto_created=True)),
                ('move_count', models.SmallIntegerField(db_index=True)),
                ('total_points', models.SmallIntegerField(db_index=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('name', models.CharField(max_length=50, default='anonymous', blank=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
