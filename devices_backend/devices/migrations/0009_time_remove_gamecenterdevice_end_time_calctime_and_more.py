# Generated by Django 5.0 on 2024-05-25 11:17

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('devices', '0008_alter_gamecenterdevice_end_time'),
    ]

    operations = [
        migrations.CreateModel(
            name='Time',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
            ],
        ),
        migrations.RemoveField(
            model_name='gamecenterdevice',
            name='end_time',
        ),
        migrations.CreateModel(
            name='CalcTime',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('endtime', models.DateTimeField(blank=True, null=True)),
                ('device', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='devices.gamecenterdevice')),
                ('time_name', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='devices.time')),
            ],
        ),
        migrations.AddField(
            model_name='gamecenterdevice',
            name='time',
            field=models.ManyToManyField(related_name='time_owned', through='devices.CalcTime', to='devices.time'),
        ),
    ]
