# Generated by Django 4.2.13 on 2024-06-19 13:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('devices', '0039_logo_alter_invoice_invoice_type'),
    ]

    operations = [
        migrations.AlterField(
            model_name='invoice',
            name='invoice_type',
            field=models.CharField(choices=[('واصل', 'واصل'), ('مفتوح', 'مفتوح')], default='None', max_length=100, null=True),
        ),
    ]