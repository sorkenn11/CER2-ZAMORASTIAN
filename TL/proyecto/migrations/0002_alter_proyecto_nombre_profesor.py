# Generated by Django 5.0.6 on 2024-05-30 00:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('proyecto', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='proyecto',
            name='nombre_profesor',
            field=models.CharField(default='-', max_length=100),
        ),
    ]
