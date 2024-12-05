# Generated by Django 5.1 on 2024-11-22 00:41

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ("condo_files", "0001_initial"),
        ("relations", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="aptinspectimages",
            name="tenant",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.DO_NOTHING,
                to="relations.condotenant",
            ),
        ),
        migrations.AddField(
            model_name="contractfiles",
            name="constract",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.DO_NOTHING, to="relations.contract"
            ),
        ),
    ]
