# Generated by Django 5.0.6 on 2024-09-25 21:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('login', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='usuario',
            name='crp',
            field=models.CharField(max_length=8, unique=True),
        ),
    ]
