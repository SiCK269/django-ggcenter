# Generated by Django 5.0 on 2024-05-25 10:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('devices', '0005_alter_refreshments_quantity'),
    ]

    operations = [
        migrations.AlterField(
            model_name='gamecenterdevice',
            name='id',
            field=models.IntegerField(editable=False, primary_key=True, serialize=False),
        ),
    ]
