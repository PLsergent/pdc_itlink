# Generated by Django 2.1.3 on 2018-11-20 14:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pdc_core_app', '0006_auto_20181120_1447'),
    ]

    operations = [
        migrations.CreateModel(
            name='AffectationActivite',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
        ),
        migrations.CreateModel(
            name='AffectationProjets',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
        ),
        migrations.AlterField(
            model_name='repartitionactivite',
            name='list_RA',
            field=models.ManyToManyField(db_table='AffectationProjets', to='pdc_core_app.RDate'),
        ),
        migrations.AlterField(
            model_name='repartitionprojet',
            name='list_R',
            field=models.ManyToManyField(db_table='AffectationActivite', to='pdc_core_app.RDate'),
        ),
    ]
