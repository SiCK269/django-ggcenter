# Generated by Django 5.0 on 2024-05-25 10:58

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('devices', '0006_alter_gamecenterdevice_id'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Refreshments',
            new_name='Refreshment',
        ),
    ]