# Generated by Django 2.1.3 on 2018-11-20 16:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pdc_core_app', '0014_auto_20181120_1614'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='affectationprojets',
            name='date',
        ),
        migrations.RemoveField(
            model_name='affectationprojets',
            name='repartitionprojet',
        ),
        migrations.AlterField(
            model_name='repartitionprojet',
            name='list_R',
            field=models.ManyToManyField(to='pdc_core_app.RDate'),
        ),
        migrations.DeleteModel(
            name='AffectationProjets',
        ),
    ]
