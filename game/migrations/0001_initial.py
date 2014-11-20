# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Cavern',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True, serialize=False)),
                ('title', models.TextField(blank=True, default='')),
                ('description', models.TextField(blank=True, default='')),
                ('link', models.CharField(blank=True, default='', max_length=1000)),
                ('points', models.SmallIntegerField(default=0)),
                ('is_entrance', models.BooleanField(default=False)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Color',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True, serialize=False)),
                ('color', models.CharField(blank=True, default='', max_length=200)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='cavern',
            name='color',
            field=models.ForeignKey(to='game.Color'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='cavern',
            name='connections',
            field=models.ManyToManyField(to='game.Cavern', related_name='connections_rel_+'),
            preserve_default=True,
        ),
    ]
