# Generated by Django 5.1 on 2024-11-02 01:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('places', '0005_remove_place_state_alter_place_city'),
    ]

    operations = [
        migrations.AddField(
            model_name='place',
            name='complement',
            field=models.CharField(max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='place',
            name='neighborhood',
            field=models.CharField(default='haha', max_length=255),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='place',
            name='street',
            field=models.CharField(max_length=255),
        ),
    ]