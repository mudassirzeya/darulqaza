# Generated by Django 3.2.5 on 2022-06-17 11:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('darul', '0006_auto_20220615_0118'),
    ]

    operations = [
        migrations.AlterField(
            model_name='case',
            name='accused',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='case',
            name='aditional_text',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='case',
            name='plaintiff',
            field=models.TextField(blank=True, null=True),
        ),
    ]
