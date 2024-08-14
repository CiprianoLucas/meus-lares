# Generated by Django 5.1 on 2024-08-14 18:22

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('places', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name='places',
            name='representative',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='place_representative', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='places',
            name='residents',
            field=models.ManyToManyField(related_name='place_residents', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='places',
            name='unions',
            field=models.ManyToManyField(related_name='place_unions', to=settings.AUTH_USER_MODEL),
        ),
    ]
