# Generated by Django 2.1.3 on 2018-11-20 14:56

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('pdc_core_app', '0007_auto_20181120_1454'),
    ]

    operations = [
        migrations.DeleteModel(
            name='AffectationActivite',
        ),
        migrations.DeleteModel(
            name='AffectationProjets',
        ),
    ]
