# Generated by Django 4.1.2 on 2022-10-18 14:02

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('Baedin_app', '0005_categories'),
    ]

    operations = [
        migrations.CreateModel(
            name='Store',
            fields=[
                ('Id', models.AutoField(primary_key=True, serialize=False)),
                ('store_name', models.TextField(blank=True, default='', null=True)),
                ('store_logo', models.TextField(blank=True, default='', null=True)),
                ('creation_time', models.DateTimeField(default=django.utils.timezone.now)),
                ('isDeleted', models.BooleanField(default=False)),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Baedin_app.categories')),
                ('userId', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
