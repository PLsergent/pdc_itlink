# Generated by Django 2.1.3 on 2018-11-20 14:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pdc_core_app', '0008_auto_20181120_1456'),
    ]

    operations = [
        migrations.AlterField(
            model_name='repartitionactivite',
            name='list_RA',
            field=models.ManyToManyField(to='pdc_core_app.RDate'),
        ),
        migrations.AlterField(
            model_name='repartitionprojet',
            name='list_R',
            field=models.ManyToManyField(to='pdc_core_app.RDate'),
        ),
    ]
