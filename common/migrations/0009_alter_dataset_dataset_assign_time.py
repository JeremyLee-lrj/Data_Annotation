# Generated by Django 4.2.8 on 2024-01-19 06:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('common', '0008_alter_session_session_last_login_month_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='dataset',
            name='dataset_assign_time',
            field=models.TextField(max_length=200),
        ),
    ]
