# Generated by Django 5.0 on 2024-05-30 21:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('devices', '0022_remove_invoice_slug'),
    ]

    operations = [
        migrations.AlterField(
            model_name='calctime',
            name='start_time',
            field=models.DateTimeField(null=True),
        ),
    ]
