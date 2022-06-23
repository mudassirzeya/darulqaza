# Generated by Django 3.2.5 on 2022-06-18 14:58

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('darul', '0010_timeline'),
    ]

    operations = [
        migrations.AddField(
            model_name='case',
            name='status',
            field=models.CharField(blank=True, choices=[('New', 'New'), ('Notice Served', 'Notice Served'), ('Mediation Completed', 'Mediation Completed'), ('Pending on Witness', 'Pending on Witness')], max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='case',
            name='case_type',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='darul.casetype'),
        ),
    ]