# -*- coding: utf-8 -*-
# Generated by Django 1.11.14 on 2018-08-12 20:21
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('lightbox_gallery_plugin', '0002_lightboxgallerycmsplugin'),
    ]

    operations = [
        migrations.AddField(
            model_name='lightboxgallerycmsplugin',
            name='justify',
            field=models.CharField(blank=True, choices=[('justify-content-left', 'Justify left'), ('justify-content-center', 'Justify center'), ('justify-content-right', 'Justify right')], default='justify-content-left', max_length=256, null=True),
        ),
    ]
