# Generated by Django 5.1 on 2024-08-14 21:38

import uuid
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('places', '0003_alter_places_number_alter_places_street'),
    ]

    operations = [
        migrations.AlterField(
            model_name='places',
            name='id',
            field=models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False),
        ),
    ]
