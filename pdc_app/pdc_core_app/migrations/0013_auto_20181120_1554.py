# Generated by Django 2.1.3 on 2018-11-20 15:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pdc_core_app', '0012_auto_20181120_1547'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='affectationa',
            name='date',
        ),
        migrations.RemoveField(
            model_name='affectationa',
            name='repartitionactivite',
        ),
        migrations.RemoveField(
            model_name='affectationp',
            name='date',
        ),
        migrations.RemoveField(
            model_name='affectationp',
            name='repartitionprojet',
        ),
        migrations.RemoveField(
            model_name='commande',
            name='collaborateurs',
        ),
        migrations.RemoveField(
            model_name='repartitionactivite',
            name='list_RA',
        ),
        migrations.AddField(
            model_name='repartitionactivite',
            name='list_RA',
            field=models.ManyToManyField(to='pdc_core_app.RDate'),
        ),
        migrations.RemoveField(
            model_name='repartitionprojet',
            name='list_R',
        ),
        migrations.AddField(
            model_name='repartitionprojet',
            name='list_R',
            field=models.ManyToManyField(to='pdc_core_app.RDate'),
        ),
        migrations.DeleteModel(
            name='AffectationA',
        ),
        migrations.DeleteModel(
            name='AffectationP',
        ),
    ]
