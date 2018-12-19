# Generated by Django 2.1.4 on 2018-12-19 08:55

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('pdc_core_app', '0016_auto_20181218_1832'),
    ]

    operations = [
        migrations.AlterField(
            model_name='commande',
            name='equipe',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='pdc_core_app.Equipe'),
        ),
        migrations.AlterField(
            model_name='repartitionactivite',
            name='activite',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='pdc_core_app.Activite'),
        ),
        migrations.AlterField(
            model_name='repartitionactivite',
            name='collaborateur',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='pdc_core_app.Collaborateur'),
        ),
        migrations.AlterField(
            model_name='repartitionprojet',
            name='collaborateur',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='pdc_core_app.Collaborateur'),
        ),
        migrations.AlterField(
            model_name='repartitionprojet',
            name='commande',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='pdc_core_app.Commande'),
        ),
        migrations.AlterField(
            model_name='responsable_e',
            name='equipe',
            field=models.OneToOneField(on_delete=django.db.models.deletion.PROTECT, to='pdc_core_app.Equipe'),
        ),
    ]
