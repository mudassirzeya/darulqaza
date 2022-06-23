# Generated by Django 3.2.5 on 2022-06-14 19:48

from django.db import migrations, models
import django.db.models.deletion
import sqlalchemy.sql.expression


class Migration(migrations.Migration):

    dependencies = [
        ('darul', '0005_rename_court_name_casetype_case_type'),
    ]

    operations = [
        migrations.AddField(
            model_name='case',
            name='case_type',
            field=models.ForeignKey(blank=True, null=sqlalchemy.sql.expression.true, on_delete=django.db.models.deletion.PROTECT, to='darul.casetype'),
            preserve_default=sqlalchemy.sql.expression.true,
        ),
        migrations.AlterField(
            model_name='case',
            name='date',
            field=models.DateField(blank=True, null=True),
        ),
    ]