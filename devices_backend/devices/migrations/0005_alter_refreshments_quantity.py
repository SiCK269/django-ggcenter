# Generated by Django 5.0 on 2024-05-24 23:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('devices', '0004_alter_gamecenterdevice_end_time'),
    ]

    operations = [
        migrations.AlterField(
            model_name='refreshments',
            name='quantity',
            field=models.IntegerField(),
        ),
    ]