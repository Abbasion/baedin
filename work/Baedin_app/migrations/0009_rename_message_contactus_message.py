# Generated by Django 4.1.2 on 2022-10-21 08:09

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Baedin_app', '0008_contactus'),
    ]

    operations = [
        migrations.RenameField(
            model_name='contactus',
            old_name='Message',
            new_name='message',
        ),
    ]
