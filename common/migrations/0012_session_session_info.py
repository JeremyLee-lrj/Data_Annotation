# Generated by Django 4.2.8 on 2024-01-22 03:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('common', '0011_alter_dataset_dataset_assign_time'),
    ]

    operations = [
        migrations.AddField(
            model_name='session',
            name='session_info',
            field=models.TextField(default='@&YBKSNDKW'),
            preserve_default=False,
        ),
    ]
