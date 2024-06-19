# Generated by Django 5.0 on 2024-06-05 08:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('devices', '0025_remove_gamecenterdevice_invoice_type_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='gamecenterdevice',
            name='time',
        ),
        migrations.AlterField(
            model_name='calctime',
            name='time_name',
            field=models.CharField(choices=[('فردي', 'فردي'), ('زوجي', 'زوجي')], default='فردي', max_length=100),
        ),
        migrations.DeleteModel(
            name='Time',
        ),
    ]