# Generated by Django 3.2.5 on 2022-06-14 16:24

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('darul', '0004_casetype'),
    ]

    operations = [
        migrations.RenameField(
            model_name='casetype',
            old_name='court_name',
            new_name='case_type',
        ),
    ]
