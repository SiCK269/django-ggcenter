# Generated by Django 5.0 on 2024-05-25 11:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('devices', '0007_rename_refreshments_refreshment'),
    ]

    operations = [
        migrations.AlterField(
            model_name='gamecenterdevice',
            name='end_time',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]
