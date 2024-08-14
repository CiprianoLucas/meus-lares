# Generated by Django 5.1 on 2024-08-14 18:22

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Images',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(upload_to='requests')),
            ],
        ),
        migrations.CreateModel(
            name='Request',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255)),
                ('description', models.CharField(max_length=20)),
                ('type', models.CharField(choices=[('R', 'RECLAMAÇÃO'), ('M', 'MANUTENÇÃO'), ('O', 'OUTROS')], default='O', max_length=255)),
                ('status', models.CharField(choices=[('A', 'ANDAMENTO'), ('C', 'CONCLUIDO'), ('P', 'PENDENTE')], default='P', max_length=255)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'verbose_name': 'Requisição',
                'verbose_name_plural': 'Requisições',
            },
        ),
    ]
