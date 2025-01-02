# Generated by Django 5.1 on 2024-12-26 14:47

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ("bills", "0001_initial"),
        ("relations", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="breachpenalty",
            name="contract",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.DO_NOTHING, to="relations.contract"
            ),
        ),
        migrations.AddField(
            model_name="finepenalty",
            name="contract",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.DO_NOTHING, to="relations.contract"
            ),
        ),
        migrations.AddField(
            model_name="recurringfee",
            name="contract",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.DO_NOTHING, to="relations.contract"
            ),
        ),
    ]
