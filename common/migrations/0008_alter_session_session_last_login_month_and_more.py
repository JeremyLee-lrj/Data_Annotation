# Generated by Django 4.2.8 on 2024-01-16 15:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('common', '0007_session'),
    ]

    operations = [
        migrations.AlterField(
            model_name='session',
            name='session_last_login_month',
            field=models.IntegerField(null=True),
        ),
        migrations.AlterField(
            model_name='session',
            name='session_last_login_year',
            field=models.IntegerField(null=True),
        ),
    ]
