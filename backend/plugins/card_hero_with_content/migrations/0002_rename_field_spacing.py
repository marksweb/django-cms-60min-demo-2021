# Generated by Django 2.2.14 on 2020-08-03 17:03

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('card_hero_with_content', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='cardherowithcontent',
            old_name='vertical_spacing',
            new_name='spacing',
        ),
    ]