# Generated by Django 5.0 on 2024-05-25 12:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('devices', '0011_calctime_start_time_alter_calctime_created_at_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='calctime',
            name='diff',
            field=models.DurationField(null=True),
        ),
    ]
