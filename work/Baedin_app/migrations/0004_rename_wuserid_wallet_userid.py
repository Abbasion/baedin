# Generated by Django 4.1.2 on 2022-10-18 07:07

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Baedin_app', '0003_wallet'),
    ]

    operations = [
        migrations.RenameField(
            model_name='wallet',
            old_name='wuserId',
            new_name='userId',
        ),
    ]
