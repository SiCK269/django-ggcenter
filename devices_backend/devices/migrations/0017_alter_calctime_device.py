# Generated by Django 5.0 on 2024-05-26 12:32

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('devices', '0016_alter_refresh_device_alter_refresh_refreshs'),
    ]

    operations = [
        migrations.AlterField(
            model_name='calctime',
            name='device',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='devices.gamecenterdevice'),
        ),
    ]
